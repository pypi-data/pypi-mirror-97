import onetrick

@onetrick
def chainop(instance):
    class meta:
        current = instance
        outputs = list()

    class chainop:
        def __getattribute__(self, name:str):
            meta.current = getattr(meta.current, name)

            return self
    
        def __iter__(self):
            return iter(meta.outputs)
        
        def __call__(self, *args, **kwargs):
            output = meta.current(*args, **kwargs)
            meta.outputs.append(output)

            return self
        
        def __getitem__(self, key):
            return meta.outputs[key]
    
    return chainop()