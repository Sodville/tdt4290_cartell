from scipy.io import loadmat
import numpy as np
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
import time

def map_annotations_to_dict(annotations):
    output = {}
    for record in annotations[0]:
        output[record[5][0]] = {
            'bbox_x_min': record[0][0][0],
            'bbox_x_max': record[1][0][0],
            'bbox_y_min': record[2][0][0],
            'bbox_y_max': record[3][0][0],
            'class_id': record[4][0][0]
        }

    return output

def map_tags_to_list(tags):
    output = []
    for tag in tags[0]:
        output.append(tag[0])

    return output

def find_tag(tag_name, fetched_tags):
    for i, t in enumerate(fetched_tags):
        if t.name == tag_name:
            return fetched_tags.pop(i)
    
    return None

ENDPOINT = 'https://northeurope.api.cognitive.microsoft.com'

training_key = '74f4411506874b9893eb04b688c26c88'
prediction_key = '<your prediction key>'
prediction_resource_id = '<your prediction resource id>'

publish_iteration_name = 'cartellModel'

trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

# Get or create project
for p in trainer.get_projects():
    if p.name == 'Cartell Test':
        project = p
        print('Found project Cartell Test')
        break
else:
    print ('Creating project...')
    project = trainer.create_project('Cartell Test')

# Read data from disk

print('Reading tags from disk ...')
tag_data = loadmat('datasets/stanford/devkit/cars_meta.mat')
tags = map_tags_to_list(tag_data['class_names'])

print('Reading training data annotations ...')
training_data = loadmat('datasets/stanford/devkit/cars_train_annos.mat')
meta_training = map_annotations_to_dict(training_data['annotations'])

# Create or fetch tags

fetched_tags = trainer.get_tags(project.id)
print(f'Found {len(fetched_tags)} tags.')

if len(fetched_tags) <= len(tags):
    dataset_to_azure_tag_id_map = {}
    for i, tag in enumerate(tags):
        tag_obj = find_tag(tag, fetched_tags)
        if tag_obj:
            dataset_to_azure_tag_id_map[i] = tag_obj
        else:
            dataset_to_azure_tag_id_map[i] = trainer.create_tag(project.id, tag)

    print(f'Created {len(tags) - len(fetched_tags)}.')
elif len(fetched_tags) > len(tags):
    print(f'Number of fetched tags ({len(fetched_tags)}) exceed number of tags \
    read from disk ({len(tags)}). Something is probably wrong!')
    exit(-1)

# Upload images

num_tagged = trainer.get_tagged_image_count(project.id)
num_untagged = trainer.get_untagged_image_count(project.id)
if num_untagged:
    print(f'Warning! There are {num_untagged} untagged images in Azure-project.')

if (num_tagged + num_tagged) == len(meta_training):
    print(f'Found {num_tagged + num_tagged} images in project and an equal number were read from disk. Skipping image upload.')
else:
    base_image_url = 'datasets/stanford/cars_train/'
    print('Uploading images...')

    for first_image in range(1, 8145, 64):
        print(f'Uploading images {first_image} to {first_image + 63}.')
        image_list = []
        for image_num in range(first_image, min(first_image + 64, 8144)):
            file_name = f'{image_num:05}.jpg'
            with open(base_image_url + file_name, 'rb') as image_contents:
                image_list.append(
                    ImageFileCreateEntry(
                        name=file_name, 
                        contents=image_contents.read(), 
                        tag_ids=[dataset_to_azure_tag_id_map[(meta_training[file_name]['class_id']) - 1].id]
                    )
                )

        upload_result = trainer.create_images_from_files(project.id, images=image_list)
        if not upload_result.is_batch_successful:
            print('Some images batch upload failed.')
            num_dupes = 0
            for fn, image in zip([f'{i:05}.jpg' for i in range(first_image, first_image + 64)], upload_result.images):
                if image.status != 'OKDuplicate':
                    print(f'Image {fn} failed with status: {image.status}')
                else:
                    num_dupes += 1
            
            print(f'{num_dupes} images were not uploaded due to being duplicates.')

            # print('Critical error. Aborting image upload.')
            # exit(-1)

# print ("Training...")
# iteration = trainer.train_project(project.id)
# while (iteration.status != "Completed"):
#     iteration = trainer.get_iteration(project.id, iteration.id)
#     print ("Training status: " + iteration.status)
#     time.sleep(1)

# # The iteration is now trained. Publish it to the project endpoint
# trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, prediction_resource_id)
# print ("Done!")