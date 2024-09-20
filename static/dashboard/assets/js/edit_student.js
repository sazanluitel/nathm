(function ($) {
    $(document).ready(function () {
        function update_student_tables(studentDatatable, form) {
            const educationalHistoryTable = studentDatatable.DataTable({
                serverSide: true,
                info: true,
                searching: false,
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
                errorCallback: function (settings, xhr, errorthrown) {
                    console.error('DataTables Ajax error:', errorthrown);
                }
            });

            form.on("submit", function (e) {
                e.preventDefault();
                e.stopPropagation();

                const form = $(this);
                const prevBtn = form.find("[type=submit]");
                const prevHTML = prevBtn.html();

                const formData = $(this).serialize();
                $.ajax({
                    url: $(this).attr('action'),
                    type: 'POST',
                    data: formData,
                    beforeSend: function () {
                        prevBtn.attr("disabled", true).html("Please wait . . .");
                    },
                    success: function (response) {
                        educationalHistoryTable.ajax.reload();
                        form.closest(".modal").modal("hide");
                    },
                    error: function (xhr, status, error) {
                        alert('An error occurred while submitting the form.');
                    },
                    complete: function () {
                        prevBtn.attr("disabled", false).html(prevHTML);
                    }
                });
            })
        }

        const studentDatatable = $("#education_history_container table");
        const form = $("#educationHistoryForm");
        update_student_tables(studentDatatable, form);

        const englishtestTable = $("#englishtest_history_container table");
        const englishTestModal = $("#englishTestModal form");
        update_student_tables(englishtestTable, englishTestModal);

        const employmentTable = $("#employment_history_container table");
        const employmentModal = $("#employmentHistoryModal form");
        update_student_tables(employmentTable, employmentModal);
    })
})(jQuery)