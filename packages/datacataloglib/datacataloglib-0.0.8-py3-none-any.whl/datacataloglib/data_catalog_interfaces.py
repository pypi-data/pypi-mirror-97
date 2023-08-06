from typing import List
import pandas as pd

# addDataSet(..)
# {
#   "dataset": [
#     {
#       "org":"100e",
#       "project":"SGH",
#       "repository":"project_data",
#       "dataset": "patientstats.csv",
#       "description": "patient statistics info",
#       "tags": ["url-to-data", "patient"],
#        "columns": [
#          { "name": "id",
#            "description": "patient id",
#            "type": "int"
#          },
#          { "name": "name",
#            "description": "patient name",
#            "type": "string"
#          },
#          { "name": "age",
#            "description": "patient age",
#            "type": int
#          }
#          { "name": "address",
#            "description": "patient address",
#            "type": "string"
#          }
#        ]
#      }
#    ]
# }


class Dataset(object):
   __slots__ = ['org', 'project', 'repository', 'dataset', 'description', 'tags', 'columns']
   def __init__(self, org, project, repository, dataset, description, tags, columns):
            self.org = org
            self.project = project
            self.repository = repository
            self.dataset = dataset
            self.description = description
            self.tags = tags
            self.columns =columns
        
def create_addDataset(dataset_list):
    #return {"dataset": dataset_list} if len(dataset_list)>0 else None
    return  dataset_list if len(dataset_list)>0 else None

def create_entry_for_addDataset(
    org, project, repository="project_data", dataset="Image", description="", tags=[], columns=[]
):
    return {
        **({'org': org} if org is not None else {}),
        "project": project,
        "repository": repository,
        "dataset": dataset,
        "description": description,
        "tags": tags,
        "columns": columns,
    }


# {
#   "tableMetadata": [
#     {
#       "org":"100e",
#       "project":"SGH",
#       "repository":"project_data",
#       "dataset": "patientstats.csv",
#       "descriptionSource": "dvc",
#       "tags": ["versions"],
#       "description": "*Version Number:* 2\n*Version Date:* 20Jan2021"
#      }
#    ]
# }


class DatasetVersion(object):
   __slots__ = ['org', 'project', 'repository', 'dataset', 'descriptionSource', 'tags', 'description']
   def __init__(self, org, project, repository, dataset, description, descriptionSource, tags):
            self.org = org
            self.project = project
            self.repository = repository
            self.dataset = dataset
            self.descriptionSource = descriptionSource
            self.tags = tags
            self.description =description
            

def create_addDatasetVersion(tableMetadata_list):
    # return {"tableMetadata": tableMetadata_list} if len(tableMetadata_list)>0 else None
    return tableMetadata_list if len(tableMetadata_list)>0 else None


def create_entry_for_addDataSetVersion(
    org,
    project,
    repository="project_data",
    dataset="Image",
    description="",
    descriptionSource="",
    tags=[],
):
    return {
        "org": org,
        "project": project,
        "repository": repository,
        "dataset": dataset,
        "descriptionSource": descriptionSource,
        "tags": tags,
        "description": description,
    }


# {
#   "columnStatistics": [
#     {
#       "org":"100e",
#       "project":"SGH",
#       "repository":"project_data",
#       "dataset": "patientstats.csv",
#       "columns": [
#         {
#         "column":"age",
#         "statistics": [
#           {
#             "statName": "distinct values",
#             "statValue": 50,
#             "startEpoch": 00000000001,
#             "endEpoch": 00000000002
#           },
#           {
#             "statName": "min value",
#             "statValue": 7,
#             "startEpoch": 00000000001,
#             "endEpoch": 00000000002
#           },
#           {
#             "statName": "max value",
#             "statValue": 70,
#             "startEpoch": 00000000001,
#             "endEpoch": 00000000002
#           },
#           {
#             "statName": "average",
#             "statValue": 27,
#             "startEpoch": 00000000001,
#             "endEpoch": 00000000002
#           }
#           ]
#         },
#         {
#           "column":"name",
#           "statistics": [
#             {
#               "statName": "distinct values",
#               "statValue": 25,
#               "startEpoch": 00000000001,
#               "endEpoch": 00000000002
#             }
#             ]
#           }
#         ]
#     }
# }


   
class DatasetStatisticColumn(object):
   __slots__ = ['column', 'statistics']
   def __init__(self, column, statistics):
            self.column = column
            self.statistics = statistics
            

class DatasetStatistic(object):
   __slots__ = ['org', 'project', 'repository', 'dataset', 'columns']
   def __init__(self, org, project, repository, dataset, columns : List[DatasetStatisticColumn]):
            self.org = org
            self.project = project
            self.repository = repository
            self.dataset = dataset
            self.columns = columns


    

def create_addColumnStatistics(columnStatistics_list):
    #return {"columnStatistics": columnStatistics_list} if len(columnStatistics_list)>0 else None
    return columnStatistics_list if len(columnStatistics_list)>0 else None


def create_entry_for_addColumnStatistics(
    org, project, repository="project_data", dataset="Image", columns=[]
):
    return {
                "org": org,
                "project": project,
                "repository": repository,
                "dataset": dataset,
                "columns": columns,
            } if len(columns)>0 else None
        
def add_column_statistic(column_name, column_describe_dict):
    return {
        "column": column_name,
        "statistics": [
            {"statName": k, "statValue": f"{v}"}
            for k, v in column_describe_dict.items()
            if not pd.isna(v)
        ],
    }

