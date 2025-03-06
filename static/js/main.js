function sanitizeString(str) {
  str = str.replace(/[^a-z0-9áéíóúñü \.,_-]/gim, "");
  return str.trim().toLowerCase().replace(/ /g, "+");
}

const screens = {
  sm: window.matchMedia("(max-width: 640px)"),
  md: window.matchMedia("(max-width: 768px)"),
  lg: window.matchMedia("(max-width: 1024px)"),
  xl: window.matchMedia("(max-width: 1280px)"),
  "2xl": window.matchMedia("(max-width: 1536px)"),
};
$(document).ready(function () {
  try {
    $(".homeIndexingsSlick").slick({
      dots: false,
      arrows: false,
      infinite: true,
      autoplay: true,
      autoplaySpeed: 10000,
      slidesToShow: 10,
      slidesToScroll: 10,
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 6,
            slidesToScroll: 6,
            dots: false,
            arrows: false,
            infinite: true,
            autoplay: true,
            autoplaySpeed: 10000,
          },
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3,
            dots: false,
            arrows: false,
            infinite: true,
            autoplay: true,
            autoplaySpeed: 3000,
          },
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: false,
            arrows: false,
            infinite: true,
            autoplay: true,
            autoplaySpeed: 3000,
          },
        },
      ],
    });
  } catch (err) {
    console.log("Slick is not initialized")
  }

  try {
    $(".journalRankingSlick").slick({
      dots: false,
      arrows: false,
      infinite: true,
      autoplay: true,
      autoplaySpeed: 5000,
      slidesToShow: 1,
      slidesToScroll: 1,
    })
  } catch (err) {
    console.log("journalRanking slick not initialized")
  }

  $(".article-abstract-btn").on("click", function () {
    const articleId = $(this).data("article");
    const abstractBlock = $(`#article-abstract-block-${articleId}`);
    abstractBlock.toggleClass("hidden");
  });

  $(".author-link").on("click", function () {
    const authorId = $(this).data("author-id");
    window.location.href = `${window.location.origin}/publications?author=${authorId}`;
  });

  $("#navbarSearch").on("keypress", function (e) {
    if (e.which == 13) {
      window.location.href = `${window.location.origin}/search?q=${$(
        this
      ).val()}`;
    }
  });

  $("#currency").on("change", function () {
    const paytmBtn = $("#payWithPaytmBtn");
    const stripeBtn = $("#payWithStripeBtn");
    if ($(this).val() === "inr") {
      paytmBtn.removeClass("hidden");
      paytmBtn.addClass("inline-flex");
      stripeBtn.addClass("hidden");
      stripeBtn.removeClass("inline-flex");
    } else {
      paytmBtn.removeClass("inline-flex");
      paytmBtn.addClass("hidden");
      stripeBtn.removeClass("hidden");
      stripeBtn.addClass("inline-flex");
    }
  });

  function openModal(modalId) {
    const modal = $(`#${modalId}`);
    modal.css("display", "flex");
    modal.css("justify-content", "center");
    modal.css("align-items", "center");
    $("html, body").addClass("overflow-hidden");
  }

  // Function to close the modal
  function closeModal(modalId) {
    const modal = $(`#${modalId}`);
    modal.css("display", "none");
    $("html, body").removeClass("overflow-hidden");
  }

  // Event listener for opening the modal
  $(".openModal").on("click", function () {
    const modalId = $(this).data("modal-id");
    openModal(modalId);
  });

  // Event listener for closing the modal
  $(".closeModal").on("click", function () {
    const modalId = $(this).data("modal-id");
    closeModal(modalId);
  });

  // // Close the modal if the user clicks outside the modal content
  // $(window).on("click", function (event) {
  //   const modalId = $(".modal:visible").attr("id");
  //   if (modalId && !$(event.target).closest(`#${modalId}`).length) {
  //     closeModal(modalId);
  //   }
  // });

  $("#payment-form").on("submit", function (e) {
    e.preventDefault();
    $("#payment-form").addClass("hidden");
    $("#payment-loader").removeClass("hidden");

    const data = {
      csrfToken: $("#payment_csrf_token").val(),
      name: $("#payment_name").val(),
      email: $("#payment_email").val(),
      phone: $("#payment_phone").val(),
      country: $("#payment_country").val(),
      amount: $("#payment_amount").val(),
      currency: $("#payment_currency").val(),
    };
    console.log(data);
    fetch("", {
      method: "POST",
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": data.csrfToken,
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        data = JSON.parse(data);
        const origin = location.protocol + "//" + location.host;
        let options = {
          key: data.RAZORPAY_API_KEY,
          amount: data.amount,
          currency: data.currency,
          name: "iARCON International LLP",
          description: "Payment",
          image: "https://hub.iarcon.org/assets/logo-fa996dec.jpeg",
          order_id: data.order_id,
          callback_url: `${origin}/payments/callback/`,
          prefill: {
            name: data.name,
            email: data.email,
            contact: data.phone,
          },
        };
        console.log(options);
        var rzp = new Razorpay(options);
        rzp.open();
        rzp.on("payment.success", function (e) {
          console.log("success", e);
        });
      })
      .catch((error) => {
        console.error("There was a problem with your fetch operation:", error);
      });
  });

  $(".keyword-search").on("click", function () {
    function replaceNonAlphabets(input) {
      var regex = /[^a-zA-Z]+/g;
      var result = input.toLowerCase().replace(regex, "+");
      if (result.endsWith("+")) {
        result = result.slice(0, -1);
      }
      return result;
    }
    let word = $(this).data("word");
    console.log(word);
    word = replaceNonAlphabets(word);
    window.location.href = `${window.location.origin}/search?q=${word}`;
  });

  // For download-pdf-modal
  const downloadPDFModal = $("#download-pdf-modal");
  const downloadPDFModalOpen = $(".download-pdf-modal-open");
  const downloadPDFModalClose = $(".download-pdf-modal-close");

  downloadPDFModalOpen.on("click", function () {
    console.log("open")
    const articleId = $(this).data("article-id");
    $("#download-pdf-modal-articleid").val(articleId);

    $("html").css("overflow", "hidden");
    downloadPDFModal.removeClass("hidden");
  });
  downloadPDFModalClose.on("click", function () {
    $("html").css("overflow", "auto");
    downloadPDFModal.addClass("hidden");
  });
  $(document).on("click", function (event) {
    if (
      !downloadPDFModal.hasClass("hidden") &&
      !$(event.target).closest(".modal-content").length &&
      !$(event.target).is(downloadPDFModalOpen)
    ) {
      downloadPDFModal.removeClass("overflow-hidden");
      $("html").css("overflow", "auto");
      downloadPDFModal.addClass("hidden");
    }
  });
  
  // For smooth scrolling when anchor clicked
  $(document).on("click", 'a[href^="#"]', function (event) {
    event.preventDefault();

    $("html, body").animate(
      {
        scrollTop: $($.attr(this, "href")).offset().top,
      },
      500
    );
  });
});
