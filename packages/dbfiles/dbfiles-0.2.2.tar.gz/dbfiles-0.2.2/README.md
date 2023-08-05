# dbfiles
dbfiles - util for compile you sql files, csv data files, yaml, json configuration into catalog of sql files.
Creates entry.sql for installation files into database.

**install**

```
sudo pip3 install dbfiles
```

**Example of usage**
```
dbfiles --src-root test --dst-root build/test --schemas main.yaml
psql -U postgres -d test -f build/test/entry.sql
```

## lxc init

```bash
lxc init ubuntu:20.04 dbfiles
lxc config set dbfiles raw.idmap "both $UID 1000"
lxc config device add dbfiles project disk source=$PWD path=/home/ubuntu/dbfiles
lxc start dbfiles
```

## lxc login, install deps

```bash
lxc exec dbfiles -- sudo --login --user ubuntu
./dbfiles/deps.sh
```

## Run script in source code from project root

```bash
# Root schema from file
PYTHONPATH=$PWD python3 ./dbfiles/main.py --src-root test --dst-root build/test --schemas main.yaml

# Inline root schema
PYTHONPATH=$PWD python3 ./dbfiles/main.py --src-root test --dst-root build/test --inlineSchemas '{"filePath": "main.yaml", "data": {"main": [{"=#": "CREATE SCHEMA IF NOT EXISTS test"}, {"include": "schema1.yaml"}, {"include": "test2/schema2.yaml"}]}}'
```

## Example of schema.yaml

```yaml
main:
  - include: schema.yaml
  - include: schema2.yaml
  - =#: CREATE SCHEMA IF NOT EXISTS test
  - sql: table.sql
  - yaml: file.yaml =# INSERT INTO test(name, value) VALUES('{file}', '{value}')
  - yaml: file.yaml =# INSERT INTO test(key, value) VALUES('key1', '{value}'->>'key1', 'key2', '{value}'->> key2)
  - json: file.json =# INSERT INTO test(name, value) VALUES('{file}', '{value}')
  - json: file.json =# INSERT INTO test(key, value) VALUES('key1', '{value}'->>'key1', 'key2', '{value}'->> key2)
  - csv: file.csv =# COPY TO test(col1, col2, col3) FROM stdin WITH CSV HEADER
  - csv: file.csv =# COPY TO test(col1, col2, col3) FROM stdin WITH CSV
  - include: schema3.yaml
  - include: schem4.yaml

```

 * **include** - include another schema.yaml
 * **=#** - execute inline sql query
 * **sql** - execute sql file
 * **yaml** - load yaml file then execute query. {file} - yaml file path, {value} - loaded data
 * **json** - load json file then execute query. {file} - json file path, {value} - loaded data
 * **csv** - load csv file. execute query with file data after it.
