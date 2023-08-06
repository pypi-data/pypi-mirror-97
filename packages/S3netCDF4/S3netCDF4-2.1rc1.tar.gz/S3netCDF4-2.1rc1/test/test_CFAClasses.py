from S3netCDF4.CFA._CFAClasses import CFADataset, CFAGroup, CFADimension
from S3netCDF4.CFA._CFAClasses import CFAVariable
from S3netCDF4.CFA import _CFAExceptions as CFAExceptions
import unittest
from datetime import datetime

class CFADatasetTest(unittest.TestCase):

    def test_createCFADataset(self):
        # first check that a CFA Dataset can be created in the permitted
        # permutations of cfa_version and format
        timenow = datetime.isoformat(
                    datetime.now(), sep=' ', timespec='seconds'
                  )
        # test the allowed cfa_version and format permutations
        for fmt_vers in [("NETCDF3", "0.4"),
                         ("NETCDF4", "0.4"),
                         ("NETCDF4", "0.5")]:
            with self.subTest(fmt=fmt_vers[0], cfa=fmt_vers[1]):
                md_value = "Created {}".format(timenow)
                dataset_md = {"History": md_value}
                cfa_dataset = CFADataset(
                    name="test",
                    format=fmt_vers[0],
                    cfa_version=fmt_vers[1],
                    metadata=dataset_md
                )
                self.assertIsInstance(cfa_dataset, CFADataset)
                self.assertEqual(cfa_dataset.getName(), "test")
                self.assertEqual(cfa_dataset.getGroups(), [])
                self.assertEqual(cfa_dataset.getFormat(), fmt_vers[0])
                self.assertEqual(cfa_dataset.getCFAVersion(), fmt_vers[1])
                self.assertEqual(cfa_dataset.getMetadata(), dataset_md)
                self.assertEqual(cfa_dataset.metadata["History"], md_value)
                with self.assertRaises(CFAExceptions.CFAGroupError):
                    cfa_dataset.getGroup("test_group")

        # test the disallowed cfa_version and format permutation
        with self.assertRaises(CFAExceptions.CFAError):
            cfa_dataset = CFADataset(
                name="test",
                format="NETCDF3",
                cfa_version="0.5",
                metadata={"History": "Created {}".format(timenow)}
            )

    def test_createCFAGroup(self):
        # first create a CFA Dataset, then create CFA groups to add to the
        # dataset
        timenow = datetime.isoformat(
                    datetime.now(), sep=' ', timespec='seconds'
                  )
        # test creation
        # note - even though netCDF3 does not support groups in the netCDF
        # file, CFA v0.4 that writes to netCDF3 supports CFAGroups as the
        # CFAGroup information is written to the variable attribute data
        for fmt_vers in [("NETCDF3", "0.4"),
                         ("NETCDF4", "0.4"),
                         ("NETCDF4", "0.5")]:
            with self.subTest(fmt=fmt_vers[0], cfa=fmt_vers[1]):
                cfa_dataset = CFADataset(
                    name="test",
                    format=fmt_vers[0],
                    cfa_version=fmt_vers[1],
                    metadata={"History": "Created {}".format(timenow)}
                )
                md_value = "CFA group"
                group_md = {"Attribute" : md_value}
                cfa_group = cfa_dataset.createGroup(
                                "test_group",
                                metadata=group_md
                            )
                self.assertIsInstance(cfa_group, CFAGroup)
                self.assertEqual(cfa_group.getName(), "test_group")
                self.assertEqual(cfa_group.getVariables(), [])
                self.assertEqual(cfa_group.getDimensions(), [])
                self.assertEqual(cfa_group.getMetadata(), group_md)
                self.assertEqual(cfa_group.metadata["Attribute"], md_value)

                self.assertEqual(cfa_group.getDataset(), cfa_dataset)
                self.assertEqual(cfa_dataset.getGroup("test_group"), cfa_group)
                self.assertEqual(cfa_dataset["test_group"], cfa_group)

                with self.assertRaises(CFAExceptions.CFAError):
                    cfa_dataset.cfa_version = 10

                with self.assertRaises(CFAExceptions.CFAError):
                    cfa_dataset["cfa_version"] = 10

                with self.assertRaises(CFAExceptions.CFAGroupError):
                    ret_group = cfa_dataset.getGroup("group_test")

                with self.assertRaises(CFAExceptions.CFAVariableError):
                    cfa_group.getVariable("test_var")

                with self.assertRaises(CFAExceptions.CFADimensionError):
                    cfa_group.getDimension("test_dim")

                with self.assertRaises(CFAExceptions.CFAGroupError):
                    cfa_dataset.renameGroup("group_test", "test_group")

                self.assertTrue(
                   cfa_dataset.renameGroup("test_group", "group_test")
                )

                # create group with old name
                self.assertIsInstance(
                    cfa_dataset.createGroup("test_group"),
                    CFAGroup
                )
                # test for create group with same name
                with self.assertRaises(CFAExceptions.CFAGroupError):
                    cfa_dataset.createGroup("group_test")


class CFAGroupTest(unittest.TestCase):

    def setUp(self):
        # create a CFADataset that is NETCDF4 format and v0.5 CFA
        timenow = datetime.isoformat(
                    datetime.now(), sep=' ', timespec='seconds'
                  )
        self.cfa_dataset = CFADataset(
            name="test",
            format="NETCDF4",
            cfa_version="v0.5",
            metadata={"History": "Created {}".format(timenow)}
        )
        # create a default group
        md_value = "CFA group"
        group_md = {"Attribute" : md_value}
        self.cfa_group = self.cfa_dataset.createGroup(
                            "test_group",
                            metadata=group_md
                         )

    def test_createVariable(self):
        

    def test_createDimension(self):
        # test the createDimension function on the self.cfa_group
        # test the Dimension created as well to ensure it's empty
        md_value = "CFA dimension"
        dim_md = {"Attribute" : md_value}
        cfa_dimension = self.cfa_group.createDimension(
                            dim_name="dimension_X",
                            dim_len=10,
                            axis_type="X",
                            metadata=dim_md
                        )
        self.assertIsInstance(cfa_dimension, CFADimension)
        self.assertEqual(self.cfa_group.getDimension("dimension_X"),
                         cfa_dimension)
        self.assertEqual(cfa_dimension.getLen(), 10)
        self.assertEqual(cfa_dimension.getName(), "dimension_X")
        self.assertEqual(cfa_dimension.getAxisType(), "X")
        self.assertEqual(cfa_dimension.getMetadata(), dim_md)
        self.assertEqual(cfa_dimension.metadata, dim_md)

        # create with same name == error
        with self.assertRaises(CFAExceptions.CFADimensionError):
            self.cfa_group.createDimension(
                dim_name="dimension_X",
                dim_len=10,
                axis_type="X",
                metadata=dim_md
            )


if __name__ == '__main__':
    unittest.main()
