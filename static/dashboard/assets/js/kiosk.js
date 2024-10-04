(function ($) {
    $(document).ready(function () {
        let currentStep = 9;
        const stepContent = $('.step-content');
        const prevBtn = $('.prev-btn');
        const nextBtn = $('.next-btn');
        const totalSteps = stepContent.length;

        function updateStepIndicator(step) {
            $('.modal-steps .step').each(function () {
                const stepIndex = parseInt($(this).attr('data-step'));
                if (stepIndex === step) {
                    $(this).addClass('current').removeClass('completed');
                }
                else if (stepIndex < step) {
                    $(this).addClass('completed').removeClass('current');
                }
                else {
                    $(this).removeClass('completed current');
                }
            });
        }

        function showStep(step) {
            stepContent.hide();
            $(`.step-content[data-step="${step}"]`).show();
            updateStepIndicator(step);
            updateStepButtons(step);
        }

        function updateStepButtons(step) {
            prevBtn.prop('disabled', step === 1);
            nextBtn.toggle(step !== totalSteps);
            $('button[type="submit"]').toggle(step === totalSteps);
        }

        const validateEmail = (email) => {
            return String(email)
                .toLowerCase()
                .match(
                    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                );
        };

        function validateStep(step) {
            let isValid = true;
            // $(`.step-content[data-step="${step}"]`).find('input, select, textarea').each(function () {
            //     const fieldType = $(this).attr('type');
            //     if ($(this).prop('required') && $(this).val() === '') {
            //         $(this).addClass('is-invalid');
            //         isValid = false;
            //     } else if (fieldType === 'email' && !emailPattern.test($(this).val())) {
            //         $(this).addClass('is-invalid');
            //         isValid = false;
            //     } else {
            //         $(this).removeClass('is-invalid');
            //     }
            // });
            return isValid;
        }

        nextBtn.click(function () {
            if (validateStep(currentStep)) {
                currentStep++;
                showStep(currentStep);
            }
        });

        prevBtn.click(function () {
            currentStep--;
            showStep(currentStep);
        });
        showStep(currentStep);

        function handle_about_us_change() {
            const about_us = $(document).find("#about_us");
            if (about_us.length > 0) {
                const value = about_us.val();
                if (value === "OTHER") {
                    $(document).find("#about_us_other_container").show();
                    $(document).find("#about_us_other_container textarea").prop("required", true);
                } else {
                    $(document).find("#about_us_other_container").hide();
                    $(document).find("#about_us_other_container textarea").prop("required", false);
                }
            }
        }

        $(document).on("change", "#about_us", handle_about_us_change)
        handle_about_us_change();

        function handle_whychoose_change() {
            const why_us = $(document).find("#why_us");
            if (why_us.length > 0) {
                const value = why_us.val();
                if (value === "OTHER") {
                    $(document).find("#why_us_other_container").show();
                    $(document).find("#why_us_other_container textarea").prop("required", true);
                } else {
                    $(document).find("#why_us_other_container").hide();
                    $(document).find("#why_us_other_container textarea").prop("required", false);
                }
            }
        }

        $(document).on("change", "#why_us", handle_whychoose_change)
        handle_whychoose_change();

        $(document).on("click", ".clearForm", function () {
            if (confirm("Are you sure want to clear form?")) {
                $(document).find(".scrollable-form form")[0].reset();
            }
        })

        const canvas = document.querySelector("canvas");
        if (canvas) {
            const signaturePad = new SignaturePad(canvas);

            $(document).on("click", "#signatureModal .btn-primary", function () {
                if (!signaturePad.isEmpty()) {
                    const dataURL = signaturePad.toDataURL("image/png");
                    const signature_preview = $(document).find("#signature_preview");
                    signature_preview.attr("src", dataURL)
                    signature_preview.parent().addClass("added");

                    fetch(dataURL)
                        .then(res => res.blob())
                        .then(blob => {
                            const file = new File([blob], "signature.png", {type: "image/png"});
                            const dataTransfer = new DataTransfer();
                            dataTransfer.items.add(file);
                            const fileInput = document.getElementById("signature-file");
                            fileInput.files = dataTransfer.files;
                            $(document).find("#signature-file").trigger("change");
                        });
                    $("#signatureModal").modal("hide");
                }
            })

            $(document).on("click", "#signatureModal .btn-secondary", function () {
                if (!signaturePad.isEmpty()) {
                    if (confirm("Are you sure want to clear signature?")) {
                        signaturePad.clear();
                    }
                }
            })
        }
    })
})(jQuery);

document.addEventListener('DOMContentLoaded', function() {
    function updateTableCell(inputField, className) {
        const value = inputField.value;
        const labelCell = document.querySelector(`.${className}`);
        if (labelCell) {
            labelCell.textContent = value;
        }
    }

    const inputs = [
        {name: 'first_name', className: 'first_name_label'},
        {name: 'middle_name', className: 'middle_name_label'},
        {name: 'last_name', className: 'last_name_label'},
        {name: 'gender', className: 'gender_label'},
        {name: 'date_of_birth_in_ad', className: 'dob_label'},
        {name: 'email', className: 'email_label'},
        {name: 'temporary-address', className: 'address_label'},
        {name: 'temporary-city', className: 'city_label'},
        {name: 'temporary-province', className: 'province_label'},
        {name: 'temporary-country', className: 'country_label'},
        {name: 'temporary-postcode', className: 'postal_code_label'},
        {name: 'temporary-contact_number', className: 'contact_num_label'},
        {name: 'permanent-address', className: 'permanent_address_label'},
        {name: 'permanent-city', className: 'permanent_city_label'},
        {name: 'permanent-province', className: 'permanent_province_label'},
        {name: 'permanent-country', className: 'permanent_country_label'},
        {name: 'permanent-postcode', className: 'permanent_postal_code_label'},
        {name: 'permanent-contact_number', className: 'permanent_contact_num_label'},
        {name: 'emergency_contact-name', className: 'emergency_contact_name_label'},
        {name: 'emergency_contact-relationship', className: 'emergency_contact_relationship_label'},
        {name: 'emergency_contact-email', className: 'emergency_contact_email_label'},
        {name: 'emergency_address-address', className: 'emergency_contact_address_label'},
        {name: 'emergency_address-city', className: 'emergency_contact_city_label'},
        {name: 'emergency_address-province', className: 'emergency_contact_province_label'},
        {name: 'emergency_address-country', className: 'emergency_contact_country_label'},
        {name: 'emergency_address-postcode', className: 'emergency_contact_postal_code_label'},
        {name: 'emergency_address-contact_number', className: 'emergency_contact_num_label'},
        {name: 'student-father_occupation', className: 'fathers_occupation_label'},
        {name: 'student-mother_occupation', className: 'mothers_occupation_label'},
        {name: 'student-annual_income', className: 'annual_income_label'},
        {name: 'student-members_in_family', className: 'family_members_label'},
        {name: 'student-payment_by', className: 'payment_by_label'},
        {name: 'student-organization', className: 'organization_label'},
        {name: 'payment-address', className: 'payment_address_label'},
        {name: 'payment-city', className: 'payment_city_label'},
        {name: 'payment-province', className: 'payment_province_label'},
        {name: 'payment-country', className: 'payment_country_label'},
        {name: 'payment-postcode', className: 'payment_postal_code_label'},
        {name: 'payment-contact_number', className: 'payment_contact_num_label'},
        {name: 'student-about_us_other', className: 'about_us_label'},
        {name: 'student-why_us', className: 'why_choose_us_label'},
        {name: 'student-why_us_other', className: 'signature_label'},
    ];
    
    inputs.forEach(input => {
        const field = document.querySelector(`input[name="${input.name}"], textarea[name="${input.name}"], select[name="${input.name}"]`);
        if (field) {
            field.addEventListener('change', function() {
                updateTableCell(field, input.className);
            });
        }
    });
    
});