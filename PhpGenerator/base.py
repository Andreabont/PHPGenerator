from os import linesep

class PhpWriteHelper:
    
    php_indent_number = 4

    def __init__(self, indent_number:str = 4):
        self.php_indent_number = indent_number

    def addCodeLines(self, code:list, lines = '', deep:int = 0):
        if type(lines) is not list:
            lines = [lines]
        for line in lines:
            if not line.endswith(linesep):
                code.append((' ' * (self.php_indent_number * deep)) + line + linesep)
            else:
                code.append((' ' * (self.php_indent_number * deep)) + line)

    def addDocLines(self, code:list, lines, deep:int = 0):
        if not lines: return
        self.addCodeLines(code, "/**", deep)
        if type(lines) is not list:
            lines = [lines]
        for line in lines:
            self.addCodeLines(code, " * %s" % line, deep)
        self.addCodeLines(code, " */", deep)

class PhpFileDeclare():
    
    declare_name = ''
    declare_assign = ''
    
    def __init__(self, name:str, assign:str):
        self.declare_name = name
        self.declare_assign = assign

    def getCodeLines(self, helper) -> list:
        return "%s=%s" % (self.declare_name, self.declare_assign)

class PhpFileUse():
    
    use_path = ''
    use_alias = None
    
    def __init__(self, path:str, alias:str = None):
        self.use_path = path
        self.use_alias = alias

    def getCodeLines(self, helper) -> list:
        code = []
        if self.use_alias:
            helper.addCodeLines(code, "use %s as %s;" % (self.use_path, self.use_alias))
        else:
            helper.addCodeLines(code, "use %s;" % (self.use_path))
        return code

class PhpFile(object):
    
    php_namespace = None
    php_declare = []
    php_uses = []
    php_helper = None
    
    def __init__(self, indent_number:str = 4):
        self.php_namespace = None
        self.php_declare = []
        self.php_uses = []
        self.php_helper = PhpWriteHelper(indent_number)
    
    def setNamespace(self, namespace:str):
        self.php_namespace = namespace
        return self
        
    def addUse(self, use:PhpFileUse):
        self.php_uses.append(use)
        return self
    
    def addDeclare(self, declare:PhpFileDeclare):
        self.php_declare.append(declare)
        return self

    def getCodeLines(self) -> list:
        code = []
        self.php_helper.addCodeLines(code, "<?php")
        self.php_helper.addCodeLines(code)
        if self.php_declare is not None:
            delcare_array = [x.getCodeLines(self.php_helper) for x in self.php_declare]
            print(delcare_array)
            self.php_helper.addCodeLines(code, "declare(%s);" % (", ".join(delcare_array)))
            self.php_helper.addCodeLines(code)    
        if self.php_namespace is not None:
            self.php_helper.addCodeLines(code, "namespace %s;" % self.php_namespace)
            self.php_helper.addCodeLines(code)
        if self.php_uses:
            for use in self.php_uses:
                self.php_helper.addCodeLines(code, use.getCodeLines(self.php_helper))
            self.php_helper.addCodeLines(code)
        return code

