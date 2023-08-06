def to_json_schema(schema, options={}):
    toReturn = {}
    nullable = False
    for k,v in schema.items():
        print(k,v)
        if(k=="nullable"): 
            nullable=True
        elif(k=="properties" or k=="patternProperties" or k=="x-patternProperties"): 
            print("recursive call on", k)
            toReturn[k] = {sk:convert_to_jsonschema(sv) for sk,sv in v.items()}
        elif(k=="items"): 
            print("recursive call on", k, v)
            toReturn[k] = convert_to_jsonschema(v)
        else:
            toReturn[k] = v
    if(nullable):
        if(not "type" in toReturn):
            toReturn["type"] = ["null"]
        elif(isinstance(toReturn["type"],str)):
            toReturn["type"] = [toReturn["type"], "null"]
        else:
            toReturn["type"] = toReturn["type"] + ["null"]            

            
    return toReturn
