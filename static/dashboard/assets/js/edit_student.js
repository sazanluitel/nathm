(function ($) {
    $(document).ready(function () {
        const studentDatatable = $(document).find(".student-datatable");
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
    })

    $(document).on("submit", ".educationHistoryForm", function (e) {
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
            beforeSend: function(){
                prevBtn.attr("disabled", true).html("Please wait . . .");
            },
            success: function (response) {
                educationalHistoryTable.ajax.reload();
                form.closest(".modal").modal("hide");
            },
            error: function (xhr, status, error) {
                alert('An error occurred while submitting the form.');
            },
            complete: function(){
                prevBtn.attr("disabled", false).html(prevHTML);
            }
        });
    })
})(jQuery)