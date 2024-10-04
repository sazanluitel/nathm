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