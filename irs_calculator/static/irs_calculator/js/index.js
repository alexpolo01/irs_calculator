$(() => {
  $(document).on("click", ".submit", function () {
    const annual_income = $("#annual_income").val();
    const filing_status = $("#filing_status").val();
    const adjustments = $("#adjustments").val();
    const federal_tax_witheld = $("#federal_tax_witheld").val();

    if (!annual_income) {
      alert("Enter annual income");
      return;
    }
    if (!filing_status) {
      alert("Enter filing status");
      return;
    }

    $.ajax({
      url: "..\\compute_tax",
      data: {
        annual_income: annual_income,
        filing_status: filing_status,
        adjustments: adjustments,
        federal_tax_witheld: federal_tax_witheld,
      },
      beforeSend: function (xhr, settings) {
        csrf_method(xhr, settings);
      },
      success: function (response) {
        let result = `Total Tax Liability : $${response.tax_liability}<br>`;
        result += `Federal Tax Withheld : $${response.federal_tax_witheld}<br>`;
        if (Number(response.refund) > 0) {
          result += `Refund Owned : $${response.refund}<br>`;
        } else {
          result += `For Payment : $${response.for_payment}<br>`;
        }
        $("#result").html(result);
      },
      error: function (response) {
        console.log("Error");
        console.log(response);
        showMessage("error", "Update Unsuccessful");
      },
    });
  });

  function csrf_method(xhr, settings) {
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    }
  }

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?

        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function showMessage(type, message) {
    Swal.fire({
      type: type,
      title: message,
    });
  }
});
