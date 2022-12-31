from constants import Tables

FETCH_PIPELINE_USER_ID_QUERY = """
SELECT
  pipeline_user_id
FROM
  %s
WHERE
  user_id = {user_id}
AND
  pipeline_name = {pipeline_name}
""" % Tables.USER_MASTER

FETCH_PIPELINE_JSON_QUERY = """
SELECT
  pipeline_json 
FROM
  {table_name}
WHERE
  id = {pipeline_user_id}
"""