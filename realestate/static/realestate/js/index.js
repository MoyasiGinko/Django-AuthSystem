$(document).ready(function () {
  // Sample company data
  const companies = {
    1: {
      name: "Company One",
      details:
        "Company One is a leading real estate firm specializing in residential and commercial properties. Established in 2000, we have helped thousands of families find their dream homes.",
    },
    2: {
      name: "Company Two",
      details:
        "Company Two offers top-notch property management services and has a portfolio of premium properties across the country. We pride ourselves on our customer service and attention to detail.",
    },
    3: {
      name: "Company Three",
      details:
        "Company Three is known for its innovative approach to real estate. We offer a wide range of properties including luxury apartments, villas, and commercial spaces.",
    },
    4: {
      name: "Company Four",
      details:
        "Company Four has been at the forefront of the real estate industry for over two decades. Our expertise lies in the development of sustainable and eco-friendly properties.",
    },
    // Add more companies as needed
  };

  // Click event for company list items
  $(".company-list li").on("click", function () {
    const companyId = $(this).data("id");
    const company = companies[companyId];

    $("#company-details").html(`
            <h2>${company.name}</h2>
            <p>${company.details}</p>
        `);
  });
});
