(function ($) {
    /* 
        Toggle
         'open' class on click of element with class 'ps-hasmenu'
    */
    $.fn.hasAttr = function (name) {
        return this.attr(name) !== undefined;
    };

    $(document).on("click", ".ps-hasmenu>.ps-link", function (e) {
        e.preventDefault();

        if ($(this).parent().hasClass("open-menu")) {
            $(this).parent().find(".ps-submenu").slideUp();
        } else {
            $(this).parent().find(".ps-submenu").slideDown();
        }

        $(this).parent().toggleClass("open-menu");
    });

    $(document).ready(function () {
        $(document).find(".ps-item").removeClass("active");
        $(document).find(".ps-hasmenu").removeClass("open-menu active");
        const pathname = window.location.pathname;

        if (pathname) {
            const fineEle = $(document).find("a[href='" + pathname + "']");
            if (fineEle.length > 0) {
                fineEle.addClass("active");

                if (fineEle.closest("ul").hasClass("ps-submenu")) {
                    fineEle.closest(".ps-hasmenu").addClass("open-menu active");
                    fineEle.closest(".ps-submenu").slideDown();
                } else {
                    fineEle.closest(".ps-item").addClass("active");
                }
            }
        }
    });


    /* 
        Toggle 'ps-sidebar-hide' class on click of element with id 'sidebar-hide'
    */
    $(document).on("click", "#sidebar-hide", function (e) {
        e.preventDefault();
        $('.ps-sidebar').toggleClass("ps-sidebar-hide");
    })

    /* 
        Toggle 'mob-sidebar-active' class and show/hide menu overlay on click of element with id 'mobile-collapse'
    */
    $(document).on("click", "#mobile-collapse", function (e) {
        e.preventDefault();
        $('.ps-sidebar').toggleClass("mob-sidebar-active");
        $('.ps-sidebar').find(".ps-menu-overlay").toggleClass("d-none");
    })

    /* 
        Hide mobile sidebar and menu overlay on click of element with class 'ps-menu-overlay'
    */
    $(document).on("click", ".ps-menu-overlay", function (e) {
        e.preventDefault();
        $('.ps-sidebar').removeClass("mob-sidebar-active");
        $('.ps-sidebar').find(".ps-menu-overlay").addClass("d-none");
    })

    $(document).ready(function () {
        try {
            $(document).find('select:not(.noselect2):not(.inmodal)').each(function () {
                const isMultiple = $(this).hasAttr("multiple")
                $(this).select2({
                    multiple: isMultiple
                });
            });

            $(document).find('select.inmodal:not(.noselect2)').each(function () {
                $(this).select2({
                    dropdownParent: $(this).closest(".modal")
                });
            });
        } catch (error) {
            console.log(error);
        }
    });


    /**
     *  Tinymce editor configuration settings
     */
    const tinymceSelector = $(document).find(".tinymce");
    if (tinymceSelector.length > 0) {
        tinymce.init({
            selector: '.tinymce',
            promotion: false,
            menubar: true,
            plugins: "codesample link media image code fullscreen table autolink advlist lists autoresize emoticons wordcount",
            toolbar: [
                'bold italic underline strikethrough | subscript superscript | list bullist numlist blockquote alignleft aligncenter alignright alignjustify autolink link table',
                'formatselect autolink forecolor |  subscript superscript | outdent indent | image media emoticons | wordcount codesample fullscreen code'
            ],
            image_advtab: false,

            // external_filemanager_path: allsmarttools.adminurl + "assets/modules/filemanager/filemanager/",
            // filemanager_title: "Filemanager",
            // external_plugins: { "filemanager": allsmarttools.adminurl + "assets/modules/tinymce/plugins/responsivefilemanager/plugin.js?v=1.0.4" },
            relative_urls: false,
            remove_script_host: true,
            // document_base_url: allsmarttools.siteurl,
            toolbar_sticky: true,
            image_dimensions: false,
            image_class_list: [
                {
                    title: 'Responsive',
                    value: 'img-responsive'
                }
            ],
            table_class_list: [
                { title: 'Table Bordered', value: 'table table-bordered' },
                { title: 'None', value: '' }
            ],
            noneditable_noneditable_class: 'alert',
            min_height: 300
        });
    }
    const datatableElement = $(document).find('.datatable');
    if (datatableElement.length > 0) {
        try {
            datatableElement.DataTable({
                paging: true,
                lengthChange: true,
                searching: true,
                ordering: false,
                info: true,
                autoWidth: false,
                responsive: true,
            });
        } catch (error) {
            console.log(error);
        }
    }
    $(document).ready(function () {
        // Initialize DataTable
        const datatableAjaxElement = $(document).find('.ajaxdatatable');
        if (datatableAjaxElement.length > 0) {
            try {
                const table = datatableAjaxElement.on('init.dt', function () {
                    $(document).find(".student_lists_table .dt-container .row:first-child > div:first-child").append(`<button disabled type="button" class="btn btn-primary" id="student_create_section">Create Section</button>`)
                }).DataTable({
                    lengthChange: true,
                    serverSide: true,
                    order: [],
                    ordering: false,
                    responsive: true,
                    ajax: {
                        url: datatableAjaxElement.data("ajax"),
                        type: 'GET',
                        data: function (d) {
                            d.campus = $('#campus-filter').val();
                            d.program = $('#program-filter').val();
                            d.department = $('#department-filter').val();
                        }
                    },
                    drawCallback: function (dt) {

                    },
                    language: {
                        emptyTable: datatableAjaxElement.data("nodata") ?? 'No data available'
                    },
                    processing: true,
                    errorCallback: function (settings, xhr, errorthrown) {
                        console.error('DataTables Ajax error:', errorthrown);
                    }
                });

                // Add event listeners for dropdowns
                $('#campus-filter, #program-filter, #department-filter').change(function () {
                    table.ajax.reload();
                });

            } catch (error) {
                console.log(error);
            }
        }

        let student_ids = [];

        function enable_or_disable_button() {
            console.log(student_ids)
            const $studentCreateSection = $("#student_create_section");
            if ($studentCreateSection.length) {
                $studentCreateSection.prop("disabled", student_ids.length === 0);
            }
        }

        function updateStudentIds() {
            student_ids = $(".student_lists_table tbody input[type=checkbox]:checked").map(function () {
                return $(this).val();
            }).get();
            enable_or_disable_button();
        }

        $(document).on("change", ".student_lists_table tbody input[type=checkbox]", updateStudentIds);

        $("#allCheckbox").on("change", function (e) {
            e.preventDefault();

            const isChecked = $(this).is(":checked");
            const $checkboxes = $(".student_lists_table tbody input[type=checkbox]");
            $checkboxes.prop("checked", isChecked);
            updateStudentIds();
        });


        function populateDropdown(selector, options) {
            const $dropdown = $(selector);
            $dropdown.empty();
            $dropdown.append('<option value="">All</option>');
            options.forEach(option => {
                $dropdown.append(`<option value="${option.id}">${option.name}</option>`);
            });
        }
    });


    $(document).on('click', '.password_field .show-hide', function () {
        const parentEle = $(this).parent();
        if (parentEle.length > 0) {
            const prevType = parentEle.find("input").attr("type");
            if (prevType == 'password') {
                parentEle.find("input").attr("type", "text");
                parentEle.find("input").attr("placeholder", "Password");
                parentEle.find(".show-hide").html('<i class="fa-regular fa-eye"></i>');
            } else {
                parentEle.find("input").attr("type", "password");
                parentEle.find("input").attr("placeholder", "********");
                parentEle.find(".show-hide").html('<i class="fa-regular fa-eye-slash"></i>');
            }
        }
    });

    window.onFileHubCallback = (file, id) => {
        try {
            const findImageEle = $(document).find(`[name="${id}"]`);
            if (findImageEle.length > 0) {
                findImageEle.val(file.uri).trigger("change");

                const container = findImageEle.closest(".image_picker_container");
                if (container) {
                    container.addClass("added");
                    container.append(`<div class="image_fill_placeholder">   
                                <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="32" d="M368 368L144 144M368 144L144 368"/></svg>
                                <img src="${file.uri}" alt="PreView Image" />
                            </div>`);
                }
            }
        } catch (error) {
            console.log(error)
        }
        $.fancybox.close();
    }

    function init_fancybox() {
        const fancyboxfile = $(document).find(".openImagePicker");
        if (fancyboxfile.length > 0) {
            fancyboxfile.fancybox({
                width: 900,
                height: 300,
                type: 'iframe',
                autoScale: false
            });
        }
    }

    init_fancybox();

    $(document).on("click", ".image_picker_container svg", function () {
        const container = $(this).closest(".image_picker_container");
        container.removeClass("added");
        container.find(".image_fill_placeholder").remove();
        container.find("input").val("");
    });

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

    $(document).on("click", ".sameAsPermanent", function () {
        const address = $(document).find("[name='permanent-address']").val();
        const city = $(document).find("[name='permanent-city']").val();
        const province = $(document).find("[name='permanent-province']").val();
        const country = $(document).find("[name='permanent-country']").val();
        const postcode = $(document).find("[name='permanent-postcode']").val();
        const contactnumber = $(document).find("[name='permanent-contact_number']").val();

        console.log(address, city, province, country, postcode, contactnumber);

        $(document).find("[name='temporary-address']").val(address);
        $(document).find("[name='temporary-city']").val(city);
        $(document).find("[name='temporary-province']").val(province);
        $(document).find("[name='temporary-country']").val(country);
        $(document).find("[name='temporary-postcode']").val(postcode);
        $(document).find("[name='temporary-contact_number']").val(contactnumber);
    })

    document.addEventListener("DOMContentLoaded", function () {
        const sectionForm = document.querySelector("#addSectionModal form");

        sectionForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const formData = new FormData(sectionForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch("{% url 'student_service:sectionlist' %}", {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken
                },
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    // Add the new section data to the table
                    const sectionTable = document.querySelector(".student_lists_table tbody");
                    const newRow = document.createElement("tr");

                    newRow.innerHTML = `
                    <td>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" />
                        </div>
                    </td>
                    <td>${data.section_name}</td>
                    <td>${data.campus}</td>
                    <td>${data.program}</td>
                    <td>${data.year}</td>
                    <td>${data.semester}</td>
                    <td>${data.users.join(', ')}</td>
                    <td>
                        <!-- Add any additional action buttons here -->
                    </td>
                `;

                    sectionTable.appendChild(newRow);

                    // Reset the form and close the modal
                    sectionForm.reset();
                    const modalElement = document.getElementById("addSectionModal");
                    const modal = bootstrap.Modal.getInstance(modalElement);
                    modal.hide();
                })
                .catch(error => console.log('Error:', error));
        });
    });
})(jQuery);
