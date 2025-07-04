from obfuscrypt.obfuscrypt_base import Structure, print_structure


def test_function():
    input = Structure(class_type="Function", function_name="print")
    excepted_output = {
        "type": "Function",
        "value": "print",
        "parameters": None
    }
    assert excepted_output == print_structure(input)
    
    
def test_string():
    input = Structure(class_type="String", value="'Carlos'")
    excepted_output = {
        "type": "String",
        "value": "'Carlos'",
    }
    assert excepted_output == print_structure(input)
      

def test_identifier():
    input = Structure(class_type="Identifier", value="value")
    excepted_output = {
        "type": "Identifier",
        "value": "value",
    }
    assert excepted_output == print_structure(input)
    
    
def test_assignment_operation():
    param1 = Structure(class_type="Identifier", value="Name")
    param2 = Structure(class_type="String", value="'Roberto'")
    input = Structure(class_type="Operation", value="Assignment", parameters=[param1,param2])
    excepted_output = {
        "type": "Operation",
        "value": "Assignment",
        "parameters": [
            {
                "type": "Identifier",
                "value": "Name",
            },
                    {
                "type": "String",
                "value": "'Roberto'",
            }
        ]
    }
    assert excepted_output == print_structure(input)
    
    
def test_binary_class():
    param1 = Structure(class_type="Identifier", value="Name")
    param2 = Structure(class_type="String", value="'Roberto'")
    input = Structure(class_type="BinaryClass", value="==", parameters=[param1,param2])
    excepted_output = {
        "type": "BinaryClass",
        "value": "==",
        "parameters": [
            {
                "type": "Identifier",
                "value": "Name",
            },
                    {
                "type": "String",
                "value": "'Roberto'",
            }
        ]
    }
    assert excepted_output == print_structure(input)
    
    
def test_unary_class():
    param1 = Structure(class_type="Identifier", value="Name")
    input = Structure(class_type="UnaryClass", value="-", parameters=[param1])
    excepted_output = {
        "type": "UnaryClass",
        "value": "-",
        "parameters": [
            {
                "type": "Identifier",
                "value": "Name",
            }
        ]
    }
    assert excepted_output == print_structure(input)