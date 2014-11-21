var updateImage = function(event) {
    $(this).addClass('active').siblings().removeClass('active');
    $(this.parentNode).prev().find('img').replaceWith($('img', this).clone());
};

jQuery(function($) {
    $('.gallery').on('click', 'li', updateImage);
});
