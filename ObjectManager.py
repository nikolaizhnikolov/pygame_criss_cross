class ObjectTypes:
    SHARED = 'shared'
    STATIC = 'static'
    DYNAMIC = 'dynamic'


# Used to keep track of all the objects present in the game
# Shared objects should ideally be initialized once and only added/removed/update
# when settings change.
# Dynamic and static level objects should only be updated and
# completely overhauled for each new level scene
# TODO: Add enum for shared/static/dynamic objects and turn them all to a single dictionary
# update all objects directly there
class ObjectManager:
    INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls
        return cls

    # Shared objects are spread across levels and are not reinitialized
    # Static objects are only rendered and not update e.g. foliage, background, non-destructible terrain
    # Dynamic objects are updated first.
    # Their new state is calculated, then they are rendered along with everything else
    __objects = {ObjectTypes.SHARED: {},
                 ObjectTypes.STATIC: {},
                 ObjectTypes.DYNAMIC: {}}

    # Adds a new object of the chosen type to the manager
    # NB: This overwrites the object for the given name key, so try not to break anything
    def add_object(self, name: str, obj, obj_type: ObjectTypes):
        self.__objects.get(obj_type).update({name: obj})

    def add_objects(self, objects: dict, obj_type: ObjectTypes):
        for obj in objects:
            self.add_object(self, obj, objects.get(obj), obj_type)

    # Removes an object with a given key and returns the entry or None if not found
    def remove_object(self, name: str, obj_type: ObjectTypes):
        try:
            return self.objects.get(obj_type).pop(name)
        except KeyError:
            return None

    def get_shared_object(self, name: str):
        return self.__objects[ObjectTypes.SHARED][name]

    def add_shared_object(self, name: str, obj):
        self.add_object(self, name, obj, ObjectTypes.SHARED)

    def add_static_level_object(self, name: str, obj):
        self.add_object(self, name, obj, ObjectTypes.STATIC)

    def add_dynamic_level_object(self, name: str, obj):
        self.add_object(self, name, obj, ObjectTypes.DYNAMIC)

    def add_shared_objects(self, objects: dict):
        for obj in objects:
            self.add_shared_object(self, obj, objects.get(obj))

    def add_static_level_objects(self, objects: dict):
        for obj in objects:
            self.add_shared_object(self, obj, objects.get(obj))

    def add_dynamic_level_objects(self, objects: dict):
        for obj in objects:
            self.add_shared_object(self, obj, objects.get(obj))

    def remove_shared_object(self, name: str):
        self.remove_object(name, self.__shared_objects)

    def remove_static_level_object(self, name: str):
        self.remove_object(name, self.__static_level_objects)

    def remove_dynamic_level_object(self, name: str):
        self.remove_object(name, self.__dynamic_level_objects)

    def set_static_level_objects(self, objects: dict):
        self.__objects[ObjectTypes.STATIC] = objects

    def set_dynamic_level_objects(self, objects: dict):
        self.__objects[ObjectTypes.DYNAMIC] = objects
