from PhpGenerator.base import PhpFile, PhpFileUse

class PhpClassAttribute:
    
    var_name = ''
    var_type = None
    var_assing = None
    
    def __init__(self, var_name, var_type = None):
        self.var_name = var_name
        self.var_type = var_type
        self.var_assing = None
        
    def setAssign(self, var_assing:str):
        self.var_assing = var_assing
        return self
            
    def getCodeLines(self, helper) -> list:
        code = []
        if self.var_type:
            helper.addDocLines(code, "@var %s" % self.var_type)
        if self.var_assing:
            helper.addCodeLines(code, "protected $%s = %s;" % (self.var_name, self.var_assing))
        else:
            helper.addCodeLines(code, "protected $%s;" % (self.var_name))
        return code

class PhpClassConst:
    
    var_name = ''
    var_assing = ''
    
    def __init__(self, var_name:str, var_assing:str):
        self.var_name = var_name
        self.var_assing = var_assing

    def getCodeLines(self, helper) -> list:
        data = []
        helper.addCodeLines(data, "const %s = %s;" % (self.var_name, self.var_assing))
        return data

class PhpClassMethodParameter:
    
    var_name = ''
    var_type = None
    var_nullable = False
    var_assing = None
    
    def __init__(self, var_name:str):
        self.var_name = var_name
        self.var_type = None
        self.var_nullable = None
        self.var_assing = None
        
    def setType(self, var_type:str, nullable:bool = False):
        self.var_type = var_type
        self.var_nullable = nullable
        return self
        
    def setAssign(self, var_assing:str):
        self.var_assing = var_assing
        return self
            
    def getDocLine(self, helper) -> str:
        code = "@param "
        if self.var_type:
            code += self.var_type + ("|null" if self.var_nullable else "") + " "
        code += "$" + self.var_name
        return code
    
    def getCodeLine(self, helper) -> str:
        code = ""
        if self.var_type:
            code += ("?" if self.var_nullable else "") + self.var_type + " "
        code += "$" + self.var_name
        if self.var_assing:
           code += " = " + self.var_assing
        return code

class PhpClassMethod:
    
    var_name = None
    var_parameters = []
    var_return_type = None
    var_return_nullable = False
    var_code = '# TODO'
    
    def __init__(self, var_name):
        self.var_name = var_name
        self.var_parameters = []
        self.var_return_type = None
        self.var_return_nullable = False
        self.var_code = '# TODO'
        
    def addParameter(self, parameter:PhpClassMethodParameter):
        self.var_parameters.append(parameter)
        return self
        
    def setReturnType(self, return_type:str, nullable:bool = False):
        self.var_return_type = return_type
        self.var_return_nullable = nullable
        return self

    def setCode(self, code):
        self.var_code = code
        return self

    def getCodeLines(self, helper) -> list:
        code = []
        param_docs = []
        param_code = []
        for parameter in self.var_parameters:
            param_docs.append(parameter.getDocLine(helper))
            param_code.append(parameter.getCodeLine(helper))
        if self.var_return_type is None:
            helper.addDocLines(code, param_docs)
            helper.addCodeLines(code, "public function %s(%s) {" % (self.var_name, ", ".join(param_code)))
        else:
            helper.addDocLines(code, param_docs + ["@return %s%s" % (self.var_return_type, ("|null" if self.var_return_nullable else ""))])
            helper.addCodeLines(code, "public function %s(%s) : %s%s {" % (self.var_name, ", ".join(param_code), ("?" if self.var_return_nullable else ""), self.var_return_type))
        helper.addCodeLines(code, self.var_code, 1)
        helper.addCodeLines(code, "}")
        return code

class PhpClassFile(PhpFile):
    
    class_name = None
    class_extends = None
    class_implements = []
    class_consts = []
    class_attributes = []
    class_methods = []
    
    def __init__(self, class_name:str, indent_number:int = 3):
        super().__init__(indent_number)
        self.class_name = class_name
        self.class_extends = None
        self.class_implements = []
        self.class_consts = []
        self.class_attributes = []
        self.class_methods = []
    
    def setExtends(self, class_extends:str):
        self.class_extends = class_extends
        return self
        
    def addImplements(self, class_implements:str):
        self.class_implements.append(class_implements)
        return self

    def addConst(self, class_consts:PhpClassConst):
        self.class_consts.append(class_consts)
        return self

    def addAttribute(self, class_attributes:PhpClassAttribute):
        self.class_attributes.append(class_attributes)
        return self

    def addMethod(self, class_methods:PhpClassMethod):
        self.class_methods.append(class_methods)
        return self

    def getCodeLines(self) -> list:
        
        code = []
        code.extend(super().getCodeLines())
        
        # Header
        class_header = "class %s" % self.class_name
        if self.class_extends is not None:
            class_header += " extends %s" % self.class_extends
        if self.class_implements:
             class_header += " implements %s" % (", ".join(self.class_implements))
        class_header += " {"
        self.php_helper.addCodeLines(code, class_header)
        self.php_helper.addCodeLines(code)
        
        # Consts
        if len(self.class_consts):
            for consts in self.class_consts:
                self.php_helper.addCodeLines(code, consts.getCodeLines(self.php_helper), 1)
            self.php_helper.addCodeLines(code)

        # Attributes
        if len(self.class_attributes):
            for attributes in self.class_attributes:
                self.php_helper.addCodeLines(code, attributes.getCodeLines(self.php_helper), 1)
                self.php_helper.addCodeLines(code)

        # Methods
        if len(self.class_methods):
            for methods in self.class_methods:
                self.php_helper.addCodeLines(code, methods.getCodeLines(self.php_helper), 1)
                self.php_helper.addCodeLines(code)

        self.php_helper.addCodeLines(code, "}")
        return code

