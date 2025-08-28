
$(document).ready(function() {
    // تأخیر کوتاه برای اطمینان از لود شدن کامل عناصر
    setTimeout(function() {
        // بررسی وجود اسلایدر و راه‌اندازی
        if ($('.products-slick').length && $('.products-slick .product').length > 0) {
            // اگر اسلایدر قبلاً راه‌اندازی شده، ابتدا آن را نابود کن
            if ($('.products-slick').hasClass('slick-initialized')) {
                $('.products-slick').slick('destroy');
            }
            
            // راه‌اندازی مجدد اسلایدر
            $('.products-slick').slick({
                rtl: true,
                slidesToShow: 4,
                slidesToScroll: 1,
                autoplay: false,
                infinite: false,
                speed: 500,
                dots: false,
                arrows: true,
                draggable: true,
                swipeToSlide: true,
                touchMove: true,
                responsive: [
                    {
                        breakpoint: 1200,
                        settings: {
                            slidesToShow: 3,
                            slidesToScroll: 1
                        }
                    },
                    {
                        breakpoint: 991,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1
                        }
                    },
                    {
                        breakpoint: 768,
                        settings: {
                            slidesToShow: 2,
                            slidesToScroll: 1
                        }
                    },
                    {
                        breakpoint: 480,
                        settings: {
                            slidesToShow: 1,
                            slidesToScroll: 1
                        }
                    }
                ]
            });

            console.log('Products slider initialized successfully');
        }
    }, 300);
});
