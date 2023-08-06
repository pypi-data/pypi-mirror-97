## Changes with pybis-1.18.4

- fixed bug in returning identifiers (thanks, Fabian!)

## Changes with pybis-1.18.3

- prevent other users to read the saved token (chmod 600)
- fixed various pylint issues
- fixed «session no longer valid» message
- fixed search issues

## Changes with pybis-1.18.2

- added deletion to transaction

## Changes with pybis-1.18.1

- fixed del_parents() bug accidentally introduced in 1.18.0

## Changes with pybis-1.18.0

- speed improvement when searching for samples and dataSets and then cycling through the results
- implemented search for number comparison, date comparison, string comparison (<, >, <=, >=)
- implemented search for parents identities and properties
- fixed minor bugs when connecting

## Changes with pybis-1.17.4

- fixed another vocabularies update bug
- extended tests
- extended documentation

## Changes with pybis-1.17.3

- fixed vocabularies bug
- fixed updating vocabularies

## Changes with pybis-1.17.1

- fixed datastore bug

## Changes with pybis-1.17.0

- added caching for often used but rarely updated openBIS objects.
- if you need to create a lot of Samples, this will improve your speed a lot
- by default, caching is enabled

## Changes with pybis-1.16.2

- transaction.commit() now updates all added samples with their respective permIds

## Changes with pybis-1.16.1

- new_dataset bugfix

## Changes with pybis-1.16.0

- added support for batch creation of samples
- changed Python minimum requirement to Python 3.6
- new vocabulary and new property_type: internalNameSpace was removed
- this will cause possible incompatibilities with older versions of openBIS (< 20.10.x)

## Changes with pybis-1.15.1

- added support for date-searching
- bugfix in property-searching

## Changes with pybis-1.14.10

- bugfix when deleting dataSets
- some improvements with the documentation

## Changes with pybis-1.14.9

- quick fix of parse_jackson error in special circumstances

## Changes with pybis-1.14.7

- bugfix: no longer any error in get_samples(), get_datasets() and get_experiments() when
  properties are provided but no data was found


## Changes with pybis-1.14.6

- bugfix duplicate property-columns in get_samples() and get_datasets()

## Changes with pybis-1.14.5

- no automagic detection of mountpoint, because of Windows incompatibilities 

## Changes with pybis-1.14.4

- added new convenience methods: get_experiments, get_projects etc.

## Changes with pybis-1.14.3

- small bugfix: prevent error

## Changes with pybis-1.14.2

- properties can be provided with either upper or lowercase
- bugfix of duplicate property columns

## Changes with pybis-1.14.1

- small bugfix

## Changes with pybis-1.14.0

- use props="*" to get all properties of all samples or datasets

## Changes with pybis-1.13.0

- added symlink() method for datasets to automatically create symlinks
- added `is_symlink()` and `is_physical()` methods for dataSets
- new `o.download_prefix` attribute for `download()` and `symlink()`
- `download_prefix` defaults to `data/openbis-hostname`

## Changes with pybis-1.12.4

- fixed a bug which occured on some opeBIS instances when retrieving samples

## Changes with pybis-1.12.3

- datasets, samples and experiments now successfully return project and space attributes

## Changes with pybis-1.12.0

- added possibility to get any additional attributes in the get_samples() method
- added possibility to get any additional attributes in the get_dataSets() method

## Changes with pybis-1.11.1

- added automatically accepting host key, otherwise mount() will hang the first time 

## Changes with pybis-1.11.0

* implemented mount() and unmount() methods to mount openBIS dataStore server via SSHFS and FUSE
* implemented is_mounted() and get_mountpoint() methods
* added instructions how to install FUSE/SSHFS on Unix systems 

## Changes with pybis-1.10.8

* dataSets of kind CONTAINER now also allow download of files

## Changes with pybis-1.10.7

* made download work, even downloadUrl attribute is missing in dataSets

## Changes with pybis-1.10.6

* added possibility to download files without /original/DEFAULT folders

## Changes with pybis-1.10.5

* bugfix: creating projects

## Changes with pybis-1.10.4

* better error messages when downloading files from datastore server

## Changes with pybis-1.10.3

* print warning message when downloaded file-size does not match with promised file-size. Do not die.

## Changes with pybis-1.10.2

* typo bugfix

## Changes with pybis-1.10.1

* fixed a nasty threading bug: open threads are now closed when downloading or uploading datasets
* this bugfix avoids this RuntimeError: cannot start new thread

## Changes with pybis-1.10.0

* dataSet upload now supports zipfiles
* dataSet upload now supports files and folders
* different behaviour when providing a folder: files are no longer flattened out, structure is kept intact

## Changes with pybis-1.9.8

* new: create and update Dateset Types
* new: create and update Experiment Types
* new: create and update Material Types
* many bugfixes
* extended documentation about creating these entity types


## Changes with pybis-1.9.7

* bugfix for creating propertyTypes of type controlled vocabulary and material


## Changes with pybis-1.9.6

* bugfix when vocabulary attribute was not identical to the code of the aassigned property type


## Changes with pybis-1.9.5

* bugfixes: get_property_assignments() method fixed for dataSet-, experiment- and materialTypes


## Changes with pybis-1.9.4

* bugfix when searching for experiments or datasets of a given type


## Changes with pybis-1.9.3

* fixed documentation: add_members (not add_persons)
* bugfix role assignments of groups


## Changes with pybis-1.9.2

* searches for datasets and samples are highly improved
* search parameters can accept a code, an identifier or an openbis entity
* searching for all datasets in a project now works
* bugfixes


## Changes with pybis-1.9.1

* bugfix: controlled vocabulary


## Changes with pybis-1.9.0

* new: search, create, update and delete Property Types
* new: search, create, update and delete Plugins
* new: create and update Sample Types
* freeze entities to prevent changes
* added more tests


## Changes with pybis-1.8.5

* changed to v3 API when fetching datastores
* gen_permId to generate unique permIds used for dataSets
* support ELN-LIMS style identifiers: /SPACE/PROJECT/COLLECTION/OBJECT_CODE
* terms now can be moved either to the top or after another term


## Changes with pybis-1.8.4

* totalCount attribute added in every Things object
* totalCount will return the total number of elements matching a search
* bugfix in get_semantic_annotation method


## Changes with pybis-1.8.3

* new method for attributes: .attrs.all() will return a dict, much like .props.all()
* attributes like registrator and modifier are now returned by default


## Changes with pybis-1.8.2

* added key-lookup and setting for properties that contain either dots or dashes
* sample.props['some-weird.property-name'] = "some value"
* check for mandatory properties in samples (objects), datasets and experiments (collections)


## Changes with pybis-1.8.1

* revised documentation
* improved DataSet creation
* added missing delete function for DataSets
* wrong entity attributes will now immediately throw an error
* more DataSet creation tests
* paging tests added
* `collection` is now alias for `experiment`
* `object` is alias for `sample`


## Changes with pybis-1.8.0

* better support for fetching entity-types (dataSetTypes, sampleTypes)
* separation of propertyAssignments from entity-types
* added .get_propertyAssignments() method to all entity-types


## Changes with pybis-1.7.6

* bugfix dataset upload for relative files (e.g. ../../file or /User/username/file)
* always only the filename is added to the dataset, not the folder containing it
* corrected License file


## Changes with pybis-1.7.5

* added paging support for all search functions by providing start_with and count arguments
* make search more robust: allow get_sample('SPACE/CODE') instead of get_sample('/SPACE/CODE')
* make search more robust: allow get_sample('   20160706001644827-208   ') 
* make interface more robust (allow sample.permid instead of sample.permId)
* make properties more robust: allow get_samples(props='name') instead of get_samples(props=['name'])
* fixed bug when parent/children of more than one element was searched: o.get_experiments().get_samples().get_parents()


## Changes with pybis-1.7.4

* pyBIS now allows to create dataset-containers that contain no data themselves
* datasets now show a «kind» attribute, which can be either PHYSICAL, LINK or CONTAINER
* PropertyAssignments and other internal data are now finally nicely presented in Jupyter
* various bugfixes
* README.md is now correctly displayed
* setup.py is fixed, installation should no longer fail because of some utf-8 problems on certain machines


## Changes with pybis-1.7.3

* improved packaging information
* LICENSE included (Apache License v.2)


## Changes with pybis-1.7.2

* added server_information to openBIS connection
* bugfix: project samples are only fetched when instance supports them


## Changes with pybis-1.7.1

* fixed bug in controlled vocabulary when property name did not match the vocabulary name
* added `xxx_contained()` methods to Samples and DataSets
* updated documentation


## Changes with pybis-1.7.0

* added components and containers functionality to both datasets and samples
* `set_attributes()` no longer automatically saves the object
* tags now have to be created (and saved) before they can be assigned
* `get_tag()` now can search for more than one tag at once and supports both code and permId
* `get_tags()` now available for almost all objects, returns a dataframe
* improved and enhanced documentation


## Changes with pybis-1.6.8

* fixed bugs with parents and children of both samples and datasets
* new samples can be defined with parents / children
* `get_parents()` and `get_children()` methods now also work on new, not yet saved objects
* `get_sample()` and `get_dataset()` now also accept arrays of permIds / identifiers
* pybis now has a CHANGELOG!

