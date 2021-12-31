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
        self.addCodeLines(code, "/**", deep)
        if type(lines) is not list:
            lines = [lines]
        for line in lines:
            self.addCodeLines(code, " * %s" % line, deep)
        self.addCodeLines(code, " */", deep)

class PhpFile(object):
    
    php_namespace = None
    php_uses = []
    php_helper = None
    
    def __init__(self, indent_number:str = 4):
        self.php_namespace = None
        self.php_uses = []
        self.php_helper = PhpWriteHelper(indent_number)
    
    def setNamespace(self, namespace:str):
        self.php_namespace = namespace
        return self
        
    def addUse(self, use:str):
        self.php_uses.append(use)
        return self

    def getCodeLines(self) -> list:
        code = []
        self.php_helper.addCodeLines(code, "<?php")
        self.php_helper.addCodeLines(code)
        if self.php_namespace is not None:
            self.php_helper.addCodeLines(code, "namespace %s;" % self.php_namespace)
            self.php_helper.addCodeLines(code)
        if self.php_uses:
            for use in self.php_uses:
                self.php_helper.addCodeLines(code, "use %s;" % use)
            self.php_helper.addCodeLines(code)
        return code

