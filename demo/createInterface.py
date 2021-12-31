import PhpGenerator.PhpInterface as PG

myInterface = PG.PhpInterfaceFile("myInterface")
myInterface.setNamespace("Test\\Namespace")
myInterface.addUse("\\DateTime")
myInterface.addUse("\\Test\\ParentClass")
myInterface.addUse("\\Test\\ClassInterface")
myInterface.addConst(PG.PhpInterfaceConst("FIELD_ID","'id'"))
myInterface.addConst(PG.PhpInterfaceConst("NAME","'name'"))
myInterface.addMethod(PG.PhpInterfaceMethod("processId").addParameter(PG.PhpInterfaceMethodParameter("id").setType("int", True)).setReturnType("int", True))
print(*myInterface.getCodeLines())
