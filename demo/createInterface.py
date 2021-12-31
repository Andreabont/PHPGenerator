import PhpGenerator.PhpInterface as PG

myInterface = PG.PhpInterfaceFile("myInterface")
myInterface.setNamespace("Test\\Namespace")
myInterface.addUse(PG.PhpFileUse("\\DateTime"))
myInterface.addUse(PG.PhpFileUse("\\Test\\ParentClass"))
myInterface.addUse(PG.PhpFileUse("\\Test\\ClassInterface"))
myInterface.addConst(PG.PhpInterfaceConst("FIELD_ID","'id'"))
myInterface.addConst(PG.PhpInterfaceConst("NAME","'name'"))
myInterface.addMethod(PG.PhpInterfaceMethod("processId").addParameter(PG.PhpInterfaceMethodParameter("id").setType("int", True)).setReturnType("int", True))
print(*myInterface.getCodeLines())
