#include <sstream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "IFits.h"
#include "ZIFits.h"
#include "ProtobufIFits.h"
#include "CMakeDefs.h"


namespace py = pybind11;
using ADH::IO::ProtobufIFits;


py::object header_value(const IFits::Entry& entry) {
    switch(entry.type) {
        case 'I':
            return py::cast(std::stol(entry.value));
        case 'B':
            return py::cast(entry.value == "T");
        case 'F':
            return py::cast(std::stod(entry.value));
        default:
            return py::cast(entry.value);
    }
}

PYBIND11_MODULE(rawzfitsreader, m) {
    m.doc() = "Python bindings for the protobuf zfits file reader";

    m.attr("ADH_VERSION_MAJOR") = ADH_VERSION_MAJOR;
    m.attr("ADH_VERSION_MINOR") = ADH_VERSION_MINOR;

    py::class_<IFits>(m, "IFits")
        .def_property_readonly("header", [](const IFits& self) {return self.GetTable().keys;})
        // the lambda enables ignoring self passed if the static method is called on an instance
        // and not the class
        .def_property_readonly_static("seen_tables", [](py::object) {return IFits::listPastTables();})
    ;

    py::class_<IFits::Entry>(m, "HeaderEntry")
        .def_readonly("type", &IFits::Entry::type)
        .def_property_readonly("value", header_value)
        .def_readonly("comment", &IFits::Entry::comment)
        .def_readonly("fits_string", &IFits::Entry::fitsString)
        .def("__repr__", [](const IFits::Entry& self) {
            return "HeaderEntry(value='"
                + self.value
                + "', comment='"
                + self.comment
                + "')";
        })
    ;

    py::class_<ZIFits, IFits>(m, "ZIFits");

    py::class_<ProtobufIFits, ZIFits>(m, "ProtobufIFits")
        .def(
            py::init<const std::string&, const std::string &>(),
            py::arg("file_path"), py::arg("table_name")
        )
        .def(
            "check_if_file_is_consistent",
            &ProtobufIFits::CheckIfFileIsConsistent,
            py::arg("update_catalog") = false,
            "Check the file for defects. Raises an exception on found problems."
        )
        .def("__len__", &ProtobufIFits::getNumMessagesInTable)
        .def(
            "read_serialized_message",
            [](ProtobufIFits &fits, uint32 number) {
                if (number > fits.getNumMessagesInTable()) {
                    std::stringstream ss;
                    ss << "Index " << number << " is out of bounds for table "
                       << "with length " << fits.getNumMessagesInTable();
                    throw std::out_of_range(ss.str());
                }
                return py::bytes(fits.readSerializedMessage(number));
            },
            py::arg("message_number"),
            "Read the specified message from the table.  ``message_number`` starts at 1."
        )
    ;
}
