(function ($) {
    $(document).ready(function () {
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

        $(document).on("click", ".clearForm", function(){
            if( confirm("Are you sure want to clear form?") ){
                $(document).find(".scrollable-form form")[0].reset();
            }
        })
    })
})(jQuery);