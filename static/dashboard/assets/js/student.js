$(document).ready(function () {
    let educationFormCount = $('#id_educational_history-TOTAL_FORMS').val();
    let workFormCount = $('#id_employment_history-TOTAL_FORMS').val();
    let testFormCount = $('#id_english_test-TOTAL_FORMS').val();

    function updateFormIndex(selector, prefix, formCount) {
        $(selector).each(function (index) {
            $(this).find('input, select, textarea').each(function () {
                let name = $(this).attr('name').replace(new RegExp(prefix + '-\\d+'), prefix + '-' + index);
                let id = $(this).attr('id').replace(new RegExp(prefix + '-\\d+'), prefix + '-' + index);
                $(this).attr({ name: name, id: id });
            });
        });
    }

    $('.add_more_education').click(function () {
        let newForm = $('#form-templates .educational_history_form').clone();
        newForm.html(newForm.html().replace(/__prefix__/g, educationFormCount));
        $('#educational-history-forms').append(newForm.html());
        educationFormCount++;
        $('#id_educational_history-TOTAL_FORMS').val(educationFormCount);
        updateFormIndex('.education-form', 'educational_history', educationFormCount);
    });

    $(document).on('click', '.remove-education-form', function () {
        $(this).closest('.education-form').remove();
        educationFormCount--;
        updateFormIndex('.education-form', 'educational_history', educationFormCount);
        $('#id_educational_history-TOTAL_FORMS').val(educationFormCount);
    });

    $('.add-more').click(function () {
        let newForm = $('#form-templates .employment_history_form').clone();
        newForm.html(newForm.html().replace(/__prefix__/g, workFormCount));
        $('#work-experience-forms').append(newForm.html());
        workFormCount++;
        $('#id_employment_history-TOTAL_FORMS').val(workFormCount);
        updateFormIndex('.work-form', 'employment_history', workFormCount);
    });

    $(document).on('click', '.remove-work-form', function () {
        $(this).closest('.work-form').remove();
        workFormCount--;
        updateFormIndex('.work-form', 'employment_history', workFormCount);
        $('#id_employment_history-TOTAL_FORMS').val(workFormCount);
    });

    $('.add-more-test').click(function () {
        let newForm = $('#form-templates .english_test_form').clone();
        newForm.html(newForm.html().replace(/__prefix__/g, testFormCount));
        $('#form-container').append(newForm.html());
        testFormCount++;
        $('#id_english_test-TOTAL_FORMS').val(testFormCount);
        updateFormIndex('.test-form', 'english_test', testFormCount);
    });

    $(document).on('click', '.remove-test-form', function () {
        $(this).closest('.test-form').remove();
        testFormCount--;
        updateFormIndex('.test-form', 'english_test', testFormCount);
        $('#id_english_test-TOTAL_FORMS').val(testFormCount);
    });

    // $('#libraryForm').on('submit', function (event) {
    //     event.preventDefault();
    //     $.ajax({
    //         type: 'POST',
    //         url: '{% url "students:studentstatus" %}',  // Make sure this is the correct URL for the form submission
    //         data: $(this).serialize(),
    //         success: function (response) {
    //             $('#libraryModal').modal('hide');  // Close modal on success
    //             alert('Book request submitted successfully!');
    //             location.reload();  // Refresh page to update counts
    //         },
    //         error: function (xhr) {
    //             alert('There was an error submitting your request.');
    //         }
    //     });
    // });

    $(document).on("click", ".submitAssignmentBtn", function(){
        const assignmentId = $(this).data('id');
        const submissionId = $(this).data('submission-id');
        $(document).find("#assignmentId").val(assignmentId);
        $(document).find("#submittedId").val(submissionId);
        $(document).find("#submitAssignmentModal").modal("show");
    })
});
