(function($){
    const owl_crousel= $(".owl-carousel")
    if(owl_crousel.length>0){
        owl_crousel.owlCarousel({
            loop:true,
            autoplay: true,
            margin:20,
            center: true,
            responsiveClass:true,
            responsive:{
                0:{
                    items:1,
                    nav:true
                },
                600:{
                    items:3,
                    nav:false
                },
                1000:{
                    items:3,
                    nav:true,
                    loop:true
                }
            }
        })
    }
    /*password change */
    
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
    
    function calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) {
            strength += 1;
        }
        if (/[A-Z]/.test(password)) {
            strength += 1;
        }
        if (/[a-z]/.test(password)) {
            strength += 1;
        }
        if (/\d/.test(password)) {
            strength += 1;
        }
        if (/[^A-Za-z0-9]/.test(password)) {
            strength += 1;
        }
        return strength;
    }
    
    $(document).on("change keyup", ".password_strength_check", function (e) {
        const password = $(this).find("input").val();
        const strength = calculatePasswordStrength(password);
        const measures = ["very-weak", "weak", "medium", "strong", "very-strong"]
    
        const meter = $(this).find(".password-meter").find(".meter-section")
        meter.removeClass(measures.join(" "))
    
        const disableTarget = $(this).data("disable")
        if (disableTarget) {
            const disableEle = $(document).find(disableTarget);
            if (disableEle.length > 0) {
                disableEle.prop('disabled', true);
                if (strength >= 4) {
                    disableEle.prop('disabled', false);
                }
            }
        }
    
        measures.map((item, index) => {
            if (strength >= index + 1) {
                meter.eq(index).addClass(item)
            }
        });
    });
})(jQuery)