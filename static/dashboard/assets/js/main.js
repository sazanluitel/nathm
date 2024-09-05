(function ($) {
    /* 
        Toggle 'open' class on click of element with class 'ps-hasmenu'
    */
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
                $(this).select2();
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
        const datatableAjaxElement = $(document).find('.ajaxdatatable');
        if (datatableAjaxElement.length > 0) {
            try {
                datatableAjaxElement.DataTable({
                    lengthChange: true,
                    serverSide: true,
                    order: [],
                    ajax: {
                        url: datatableAjaxElement.data("ajax"),
                        type: 'GET'
                    },
                    drawCallback: function (dt) {
                        initializeSelect2();  // If you have custom initialization logic, replace this line.
                    },
                    language: {
                        emptyTable: datatableAjaxElement.data("nodata") ?? 'No data available'
                    },
                    processing: true,
                    errorCallback: function (settings, xhr, errorthrown) {
                        console.error('DataTables Ajax error:', errorthrown);
                    }
                });
            } catch (error) {
                console.log(error);
            }
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
            if (id === "tour_gallery_select") {
                hanlde_tour_gallery_image(file);
            } else {
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
            }
        } catch (error) {
            console.log(error)
        }
        $.fancybox.close();
    }

    const fancyboxfile = $(document).find(".openImagePicker");
    if (fancyboxfile.length > 0) {
        fancyboxfile.fancybox({
            width: 900,
            height: 300,
            type: 'iframe',
            autoScale: false
        });
    }

    $(document).on("click", ".image_picker_container svg", function () {
        const container = $(this).closest(".image_picker_container");
        container.removeClass("added");
        container.find(".image_fill_placeholder").remove();
        container.find("input").val("");
    });
})(jQuery);

$(document).ready(function () {
    $('#subcategoryTable').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "{% url 'menu:sub-category' %}",  // Ensure this matches your view's URL
            "type": "GET",
            "dataSrc": "data"
        },
        "columns": [
            { "data": "id" },
            { "data": "name" },
            { "data": "actions", "orderable": false, "searchable": false }  // Actions column, not sortable or searchable
        ]
    });
});