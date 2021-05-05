import hvac
client = hvac.Client(
    url='http://13.126.134.85:8200',
    token='s.f25apx4UamivtWigU9uCfTdt'
)
# Write a k/v pair under path: secret/foo
# create_response = client.secrets.kv.v2.create_or_update_secret(path='foo',secret=dict(baz='bar'))
# Read the data written under path: secret/foo
read_response = client.secrets.kv.read_secret_version(path='psql_db_user_password')
print(read_response)
print('Value under path "secret/foo" / key "baz": {val}'.format(val=read_response['data']['data']['password']))
