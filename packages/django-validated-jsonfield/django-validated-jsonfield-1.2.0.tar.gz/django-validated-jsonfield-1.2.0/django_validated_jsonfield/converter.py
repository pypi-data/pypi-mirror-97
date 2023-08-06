def to_json_schema(schema, options={}):
    toReturn = {}
    nullable = False
    for k,v in schema.items():
        if(k=="x-patternProperties"): k="patternProperties"

        #print(k,v)
        if(k=="nullable"): 
            nullable=True
        elif(k=="properties" or k=="patternProperties"): 
            toReturn[k] = {sk:to_json_schema(sv, options) for sk,sv in v.items()}
        elif(k=="items"): 
            toReturn[k] = to_json_schema(v, options)
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
