$(document).ready(function () {
    // Total form count variables for each formset
    let educationFormCount = $('#id_educational_history-TOTAL_FORMS').val();
    let workFormCount = $('#id_employment_history-TOTAL_FORMS').val();
    let testFormCount = $('#id_english_test-TOTAL_FORMS').val();

    // Function to dynamically update form indices
    function updateFormIndex(selector, prefix, formCount) {
        $(selector).each(function (index) {
            $(this).find('input, select, textarea').each(function () {
                let name = $(this).attr('name').replace(new RegExp(prefix + '-\\d+'), prefix + '-' + index);
                let id = $(this).attr('id').replace(new RegExp(prefix + '-\\d+'), prefix + '-' + index);
                $(this).attr({ name: name, id: id });
            });
        });
    }

    // Add new Educational History form
    $('.add_more_education').click(function () {
        let newForm = $('#form-templates .educational_history_form').clone();
        newForm.html(newForm.html().replace(/__prefix__/g, educationFormCount)); // Update prefix
        $('#educational-history-forms').append(newForm.html());
        educationFormCount++;
        $('#id_educational_history-TOTAL_FORMS').val(educationFormCount);
        updateFormIndex('.education-form', 'educational_history', educationFormCount);
    });

    // Remove Educational History form
    $(document).on('click', '.remove-education-form', function () {
        $(this).closest('.education-form').remove();
        educationFormCount--;
        updateFormIndex('.education-form', 'educational_history', educationFormCount);
        $('#id_educational_history-TOTAL_FORMS').val(educationFormCount);
    });

    // Add new Work Experience form
    $('.add-more').click(function () {
        let newForm = $('#form-templates .employment_history_form').clone();
        newForm.html(newForm.html().replace(/__prefix__/g, workFormCount)); // Update prefix
        $('#work-experience-forms').append(newForm.html());
        workFormCount++;
        $('#id_employment_history-TOTAL_FORMS').val(workFormCount);
        updateFormIndex('.work-form', 'employment_history', workFormCount);
    });

    // Remove Work Experience form
    $(document).on('click', '.remove-work-form', function () {
        $(this).closest('.work-form').remove();
        workFormCount--;
        updateFormIndex('.work-form', 'employment_history', workFormCount);
        $('#id_employment_history-TOTAL_FORMS').val(workFormCount);
    });

    // Add new English Test form
    $('.add-more-test').click(function () {
        let newForm = $('#form-templates .english_test_form').clone();
        newForm.html(newForm.html().replace(/__prefix__/g, testFormCount)); // Update prefix
        $('#form-container').append(newForm.html());
        testFormCount++;
        $('#id_english_test-TOTAL_FORMS').val(testFormCount);
        updateFormIndex('.test-form', 'english_test', testFormCount);
    });

    // Remove English Test form
    $(document).on('click', '.remove-test-form', function () {
        $(this).closest('.test-form').remove();
        testFormCount--;
        updateFormIndex('.test-form', 'english_test', testFormCount);
        $('#id_english_test-TOTAL_FORMS').val(testFormCount);
    });
});
