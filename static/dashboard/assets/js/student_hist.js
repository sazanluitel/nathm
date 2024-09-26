(function ($) {
    $(document).ready(function () {
        function update_student_tables(studentDatatable, form) {
            const educationalHistoryTable = studentDatatable.DataTable({
                serverSide: true,
                info: true,
                searching: true,
                paging: true,
                lengthChange: false,
                ajax: {
                    url: studentDatatable.data("ajax"),
                    type: 'GET'
                },
                language: {
                    emptyTable: studentDatatable.data("nodata") ?? 'No data available'
                },
                processing: true,
                error: function (xhr, error, thrown) {
                    console.error('DataTables Ajax error:', thrown);
                    alert('An error occurred while loading data. Please try again later.');
                }
            });

            // Handle form submission for adding/updating data
            form.on("submit", function (e) {
                e.preventDefault();
                e.stopPropagation();

                const prevBtn = form.find("[type=submit]");
                const prevHTML = prevBtn.html();
                const formData = form.serialize();

                $.ajax({
                    url: form.attr('action'),
                    type: 'POST',
                    data: formData,
                    beforeSend: function () {
                        prevBtn.attr("disabled", true).html("Please wait . . .");
                    },
                    success: function (response) {
                        educationalHistoryTable.ajax.reload();
                        form.closest(".modal").modal("hide");
                        form[0].reset(); // Reset form fields
                        alert('Data submitted successfully!'); // Optional success message
                    },
                    error: function (xhr, status, error) {
                        if (xhr.status === 400) {
                            alert('Bad Request: Please check your input.'); // Specific error handling
                        } else {
                            alert('An error occurred while submitting the form. Please try again later.');
                        }
                    },
                    complete: function () {
                        prevBtn.attr("disabled", false).html(prevHTML);
                    }
                });
            });
        }

        const educationalDatatable = $("#education_history_container table");
        const educationalForm = $("#educationHistoryForm");
        update_student_tables(educationalDatatable, educationalForm);

        const englishTestTable = $("#englishtest_history_container table");
        const englishTestForm = $("#englishTestModal form");
        update_student_tables(englishTestTable, englishTestForm);

        const employmentTable = $("#employment_history_container table");
        const employmentForm = $("#employmentHistoryModal form");
        update_student_tables(employmentTable, employmentForm);
    });
})(jQuery);
