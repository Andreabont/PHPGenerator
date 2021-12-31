from PhpGenerator.base import PhpFile

class PhpInterfaceConst:
    
    var_name = ''
    var_assing = ''
    
    def __init__(self, var_name:str, var_assing:str):
        self.var_name = var_name
        self.var_assing = var_assing
    
    def getCodeLines(self, helper) -> list:
        data = []
        helper.addCodeLines(data, "const %s = %s;" % (self.var_name, self.var_assing))
        return data

class PhpInterfaceMethodParameter:
    
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
class PhpInterfaceConst:
    
    var_name = ''
    var_assing = ''
    
    def __init__(self, var_name:str, var_assing:str):
        self.var_name = var_name
        self.var_assing = var_assing
    
    def getCodeLines(self, helper) -> list:
        data = []
        helper.addCodeLines(data, "const %s = %s;" % (self.var_name, self.var_assing))
        return data

class PhpInterfaceMethodParameter:
    
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

class PhpInterfaceMethod:
    
    var_name = None
    var_parameters = []
    var_return_type = None
    var_return_nullable = False
    
    def __init__(self, var_name:str):
        self.var_name = var_name
        self.var_parameters = []
        self.var_return_type = None
        self.var_return_nullable = False

    def addParameter(self, parameter:PhpInterfaceMethodParameter):
        self.var_parameters.append(parameter)
        return self
        
    def setReturnType(self, return_type:str, nullable:bool = False):
        self.var_return_type = return_type
        self.var_return_nullable = nullable
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
            helper.addCodeLines(code, "public function %s(%s);" % (self.var_name, ", ".join(param_code)))
        else:
            helper.addDocLines(code, param_docs + ["@return %s%s" % (self.var_return_type, ("|null" if self.var_return_nullable else ""))])
            helper.addCodeLines(code, "public function %s(%s) : %s%s;" % (self.var_name, ", ".join(param_code), ("?" if self.var_return_nullable else ""), self.var_return_type))
        return code

class PhpInterfaceFile(PhpFile):
    
    class_name = None
    class_consts = []
    class_methods = []
    
    def __init__(self, class_name:str, indent_number:int = 3):
        super().__init__(indent_number)
        self.class_name = class_name
        self.class_consts = []
        self.class_methods = []

    def addConst(self, class_consts:PhpInterfaceConst):
        self.class_consts.append(class_consts)
        return self

    def addMethod(self, class_methods:PhpInterfaceMethod):
        self.class_methods.append(class_methods)
        return self

    def getCodeLines(self) -> list:
        
        code = []
        code.extend(super().getCodeLines())
        
        # Header
        self.php_helper.addCodeLines(code, "interface %s {" % self.class_name)
        self.php_helper.addCodeLines(code)
        
        # Consts
        if len(self.class_consts):
            for consts in self.class_consts:
                self.php_helper.addCodeLines(code, consts.getCodeLines(self.php_helper), 1)
            self.php_helper.addCodeLines(code)

        # Methods
        if len(self.class_methods):
            for methods in self.class_methods:
                self.php_helper.addCodeLines(code, methods.getCodeLines(self.php_helper), 1)
                self.php_helper.addCodeLines(code)

        self.php_helper.addCodeLines(code, "}")
        return code

class PhpInterfaceMethod:
    
    var_name = None
    var_parameters = []
    var_return_type = None
    var_return_nullable = False
    
    def __init__(self, var_name:str):
        self.var_name = var_name
        self.var_parameters = []
        self.var_return_type = None
        self.var_return_nullable = False

    def addParameter(self, parameter:PhpInterfaceMethodParameter):
        self.var_parameters.append(parameter)
        return self
        
    def setReturnType(self, return_type:str, nullable:bool = False):
        self.var_return_type = return_type
        self.var_return_nullable = nullable
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
            helper.addCodeLines(code, "public function %s(%s);" % (self.var_name, ", ".join(param_code)))
        else:
            helper.addDocLines(code, param_docs + ["@return %s%s" % (self.var_return_type, ("|null" if self.var_return_nullable else ""))])
            helper.addCodeLines(code, "public function %s(%s) : %s%s;" % (self.var_name, ", ".join(param_code), ("?" if self.var_return_nullable else ""), self.var_return_type))
        return code

class PhpInterfaceFile(PhpFile):
    
    class_name = None
    class_consts = []
    class_methods = []
    
    def __init__(self, class_name:str, indent_number:int = 3):
        super().__init__(indent_number)
        self.class_name = class_name
        self.class_consts = []
        self.class_methods = []

    def addConst(self, class_consts:PhpInterfaceConst):
        self.class_consts.append(class_consts)
        return self

    def addMethod(self, class_methods:PhpInterfaceMethod):
        self.class_methods.append(class_methods)
        return self

    def getCodeLines(self) -> list:
        
        code = []
        code.extend(super().getCodeLines())
        
        # Header
        self.php_helper.addCodeLines(code, "interface %s {" % self.class_name)
        self.php_helper.addCodeLines(code)
        
        # Consts
        if len(self.class_consts):
            for consts in self.class_consts:
                self.php_helper.addCodeLines(code, consts.getCodeLines(self.php_helper), 1)
            self.php_helper.addCodeLines(code)

        # Methods
        if len(self.class_methods):
            for methods in self.class_methods:
                self.php_helper.addCodeLines(code, methods.getCodeLines(self.php_helper), 1)
                self.php_helper.addCodeLines(code)

        self.php_helper.addCodeLines(code, "}")
        return code

