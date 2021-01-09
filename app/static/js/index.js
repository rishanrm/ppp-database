var firstPageLoadRequest = true
var requestCount = 0
var initialConditions = true
var requestParams
var initialSortColumn = 'loanamount'
var initialFilterColumn = 'state'
var defaultFilterValue = 'AK'
var initialFilterValue
var initialStateAddition
var resetButtonClicked = false
var page = window.location.href.split('//')[1].split('/')[1]
var $table = $('#table')
var $summaryTable = $('#summary-table')
var $resetButton = $('#resetButton')
var $summaryResetButton = $('#summaryResetButton')
var stateList = ['AE','AK','AL','AR','AS','AZ','CA','CO','CT','DC'
                ,'DE','FL','GA','GU','HI','IA','ID','IL','IN','KS'
                ,'KY','LA','MA','MD','ME','MI','MN','MO','MP','MS'
                ,'MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH'
                ,'OK','OR','PA','PR','RI','SC','SD','TN','TX','UT'
                ,'VA','VI','VT','WA','WI','WV','WY']

for (let i = 0; i < 10; i++) {
    callTable(i)
}

function callTable(i) {
    setTimeout(function() {
        $table.bootstrapTable();
        // console.log('Table called time #' + i);
    }, 2000 * i);
}

// <!-- Get column options -->
var colOptions;
var cdOptions = {};

function getColumnNames() {
     // console.log(params)
    var request = new XMLHttpRequest();
    // request.open('GET', '/header_options', false);  // `false` makes the request synchronous
    request.open('GET', '/data/column_options.json', false);  // `false` makes the request synchronous
    request.send(null);

    if (request.status === 200) {
        colOptions = JSON.parse(request.responseText);
    }
}
getColumnNames()
updateCdOptions(initialFilterValue, '')

function updateCdOptions(state, cd) {
    var updatedOptionsHtml
    if (cd == '') {
        updatedOptionsHtml = '<option value selected="selected"></option>'
    } else {
        updatedOptionsHtml = '<option value></option>'
    }
    for (var [key, val] of Object.entries(colOptions.cd)) {
        if (key.includes(state)) {
            if (key == cd) {
                updatedOptionsHtml += '<option value="' + key + '" selected="selected">' + val + '</option>'
            } else {
                updatedOptionsHtml += '<option value="' + key + '">' + val + '</option>'
            }
        }
    }
    var cdColumn = document.getElementsByClassName('bootstrap-table-filter-control-cd')[0]
    if (cdColumn != undefined) {
        cdColumn.innerHTML = updatedOptionsHtml
    }
}

// <!-- Get user state from IP-->
var getUserState = new Promise((resolve, reject) => {
    if (firstPageLoadRequest) {
        var ipAddress = "";
        const key = 'sn6uiu8fba471e'

        // <!-- Get IP Address -->
        $.getJSON("https://api.ipify.org?format=json", function(data) { 
            ipAddress = data.ip
            $("#location").html(ipAddress);
            console.log(ipAddress)
        })

        // <!-- Get location -->
        const ipUrl = `https://api.ipregistry.co/${ipAddress}?key=${key}`
        console.log(ipUrl)
        try {
            fetch(ipUrl)
            .then(resp => {
                return resp.text();
            })
            .then(function(data) {
                var obj = JSON.parse(data);
                const stateCode = obj.location.region.code;
                initialFilterValue = stateCode.substr(stateCode.length - 2);
                resolve(initialFilterValue);
            })
            .catch(error => {
                reject(error)
            })
        }
        catch(error) {
            reject(error)
        }
    } else {
        resolve(initialFilterValue)
    }
})

// <!-- Get data -->
function ajaxRequest(params) {
    console.log("ENTERING AJAX REQUEST RIGHT HERE")

    getUserState
    .then(function(userStateFromIP) {
        console.log("HERE HERE HERE")
        initialFilterValue = userStateFromIP
    })
    .catch(() => {
        initialFilterValue = defaultFilterValue;
    })
    .then(value => {

        // <!-- Ensure state from IP is among the state options -->
        if (!stateList.includes(initialFilterValue)) {
            initialFilterValue = defaultFilterValue
        }

        // <!-- Set the state dropdown value to the user's state -->
        if (firstPageLoadRequest) {
            $('select[class*="bootstrap-table-filter-control-' + 'state' + '"]').val(initialFilterValue);
            firstPageLoadRequest = false;
        }
    })
    .then(value => {

        // <!-- Get column inputs on the HTML page -->
        var actualInputValues = {}
        var columns = Object.keys(orderedData)
        console.log(columns)
        for (column of columns) {
            var openFieldVal = $("#table").find("input.form-control.bootstrap-table-filter-control-" + column).val()
            if (openFieldVal != undefined && openFieldVal != '') {
                actualInputValues[column] = openFieldVal
            } else {
                var selectionVal = $('select[class*="bootstrap-table-filter-control-' + column + '"]').val();
                if (selectionVal != undefined && selectionVal != '') {
                    actualInputValues[column] = selectionVal
                }
            }
        }
        console.log("ACTUAL INPUT VALUES:")
        console.log(actualInputValues)
        updateCdOptions(actualInputValues['state'], actualInputValues['cd'])
        console.log(params)
        params.data.filter = JSON.stringify(actualInputValues)

        // <!-- Get global search box input on the HTML page -->
        var searchValue = document.querySelector("body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4 > div.fixed-table-toolbar > div.float-right.search.btn-group > div > input").value
        if (searchValue != '') {
            params.data.search = searchValue
        } else {
            delete params.data.search
        }

        // <!-- Determine if state selection in the table has been changed -->
        $('select[class*="bootstrap-table-filter-control-state"]').each(function(i) {

            // State found
            if ($(this).children('option[selected="selected"]').length != 0) {

                // New state has been selected
                if ($(this).children('option[selected="selected"]').attr('value') != initialFilterValue) {
                    initialConditions = false;
                }
            } else {
                // 'No state' option has been selected
                initialConditions = false;
            }
        });
        console.log('Request Count: ' + requestCount)
        var url = '/data'
        console.log("HERE ARE THE PARAMS IN THE REQUEST:")
        console.log($.param(params.data))
        // console.log("END PARAMS")
        // $.get(url + '?' + $.param(params.data))

        if (requestCount == 0) {

            // Customize toggle switch text
            var toggleText = $('button[name ="toggle"]').contents().filter(function() {
                return this.nodeType == Node.TEXT_NODE;
            })
            if (toggleText.prevObject[1].data === ' Toggle') {
                toggleText.prevObject[1].data = " Show card view"
            }

            // Change request params for initial table load
            requestParams = 'search=&sort='
                            + initialSortColumn
                            + '&order=desc&offset=0&limit=10&filter=%7B%22'
                            + initialFilterColumn
                            + '%22%3A%22'
                            + initialFilterValue
                            + '%22%7D'
            console.log("Manual params:")
            console.log(requestParams)
        } else {
            if (initialConditions){
                if ($.param(params.data).includes('filter')){
                    initialStateAddition = '%2C%22' + initialFilterColumn + '%22%3A%22' + initialFilterValue + '%22'
                    requestParams = $.param(params.data).substring(0, $.param(params.data).length - 3) + initialStateAddition + $.param(params.data).substring($.param(params.data).length - 3, $.param(params.data).length);
                } else {
                    initialStateAddition = '&filter=%7B%22' + initialFilterColumn + '%22%3A%22' + initialFilterValue + '%22%7D'
                    requestParams = $.param(params.data) + initialStateAddition;
                }
            } else {
                requestParams = $.param(params.data)
            }
        }
        console.log('The request params are: \r\n' + requestParams)
        console.log(url + '?' + 'page=' + page + '&' + requestParams)
        $.get(url + '?' + 'page=' + page + '&' + requestParams)
        
        .then(function (res) {
            params.success(res)
            console.log(res)
            console.log("THAT WAS THE RES")
            var thisTerm
            var businessTerm
            var stateSelected
            var loanCountTerm
            var loanTotal
            var jobsTotal
            var loanCount = res.total
            if (loanCount == 0) {
                summary = ' '
            } else {
                if (loanCount == 1) {
                    thisTerm = 'This'
                    loanCountTerm = ''
                    businessTerm = 'organization'
                } else {
                    thisTerm = 'These'
                    loanCountTerm = numberWithCommas(loanCount) + ' '
                    businessTerm = 'organizations'
                }
                loanTotal = res.footer.loanamountsum
                if (loanTotal == null) {
                    loanTotal = '$ ¯\\_(ツ)_/¯'
                }
                jobsTotal = res.footer.jobsreportedsum
                var jobsString = ' job'

                if ((jobsTotal > 1) || (jobsTotal == null) || (jobsTotal == 0)) {
                    jobsString += 's'
                }
                if (jobsTotal == null) {
                    jobsTotal = '¯\\_(ツ)_/¯'
                }
                jobsTotal = numberWithCommas(jobsTotal)
                var paramsStateIdentifier = 'state%22%3A%22'
                if (requestParams.includes(paramsStateIdentifier)) {
                    var stateIndex = requestParams.indexOf("state%22%3A%22") + paramsStateIdentifier.length;
                    stateSelected = requestParams.substring(stateIndex, stateIndex + 2);
                } else {
                    stateSelected = ''
                }

                var summary = ('<span class=\'summary-intro\'>THE GIST:</span> ' + thisTerm + ' <span class=\'summary-var\'>' + loanCountTerm + ' ' + stateSelected + ' ' + businessTerm + ' </span>received <span class=\'summary-var\'>' + loanTotal + '</span> in PPP funds to support <span class=\'summary-var\'>' + jobsTotal + '</span> ' + jobsString + '.*')
            }
                // document.getElementById("summary").innerText = summary;
            var summaryDiv = document.getElementById("summary");
            summaryDiv.innerHTML = summary;

        });
        requestCount++;
    })
};
    
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
// <!-- Format loan amount data -->        

    function amountFormatter(value) {
        // return value.substring(0, value.length - 3)
        return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    function naicsFormatter(value) {
        if (colOptions["naicscode"][value]) {
            return colOptions["naicscode"][value].replace(' ', '<br>');
        } else {
            return "Unanswered";
        }
    }

// <!-- Custom text for loading message, footer, search box placeholder, no match found -->
        
(function ($) {
    'use strict';
    $.fn.bootstrapTable.locales['en-US-custom'] = {
        formatLoadingMessage: function () {
            return 'Doing government work';
        },
        formatRecordsPerPage: function (pageNumber) {
            return pageNumber + ' results per page';
        },
        formatShowingRows: function (pageFrom, pageTo, totalRows) {
            return 'Showing ' + pageFrom.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' to ' + pageTo.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' of ' + totalRows.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' loans';
        },
        formatSearch: function () {
            return 'Search all columns';
        },
        formatNoMatches: function () {
            return '<br>Those loans don\'t exist...¯\\_(ツ)_/¯<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>';
        },
        formatExport: function () {
            return 'Export page'
        }
    };
    $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['en-US-custom']);
})(jQuery);


// <!-- Format data when a row is expanded -->
var orderedData
function getOrderedData() {
    if(page.includes('all-data')) {
        orderedData = {
            "loanamount": "Loan Amount",
            "businessname": "Business Name",
            "address": "Address",
            "city": "City",
            "state": "State",
            "zip": "ZIP Code",
            "naicscode": "Industry (NAICS Code)",
            "businesstype": "Business Type",
            "raceethnicity": "Race/Ethnicity",
            "gender": "Gender",
            "veteran": "Veteran",
            "nonprofit": "Nonprofit",
            "jobsreported": "Jobs Reported",
            "dateapproved": "Date Approved",
            "lender": "Lender",
            "cd": "House District"
        }
    } else if(page.includes('data-150k-and-up')) {
        orderedData = {
            "loanrange": "Loan Range",
            "businessname": "Business Name",
            "address": "Address",
            "city": "City",
            "state": "State",
            "zip": "ZIP Code",
            "naicscode": "Industry (NAICS Code)",
            "businesstype": "Business Type",
            "raceethnicity": "Race/Ethnicity",
            "gender": "Gender",
            "veteran": "Veteran",
            "nonprofit": "Nonprofit",
            "jobsreported": "Jobs Reported",
            "dateapproved": "Date Approved",
            "lender": "Lender",
            "cd": "House District"
        }
    } else if(page.includes('data-under-150k')) {
        orderedData = {
            "loanamount": "Loan Amount",
            "city": "City",
            "state": "State",                
            "zip": "ZIP Code",
            "naicscode": "Industry (NAICS Code)",
            "businesstype": "Business Type",
            "raceethnicity": "Race/Ethnicity",
            "gender": "Gender",
            "veteran": "Veteran",
            "nonprofit": "Nonprofit",
            "jobsreported": "Jobs Reported",
            "dateapproved": "Date Approved",
            "lender": "Lender",
            "cd": "House District"
        }
    }
}
getOrderedData()

function getOrderedColumns() {
    return Object.values(orderedData)
}

function reorderValues(row) {
    var orderedValues = []
    $.each(Object.keys(orderedData), function(index, value) {
        orderedValues.push(row[value])
    })
    return orderedValues
}

function formatValues(values) {
    var i;
    for (i = 0; i < values.length; i++) { 
        if (values[i] == null) {
            values[i] = "Unanswered"
        }
    }
    return values
}

function detailFormatter(index, row) {
    var orderedColumns = getOrderedColumns()
    var orderedValues = reorderValues(row)
    orderedValues = formatValues(orderedValues)

    var html = ['<div class="detailview">']
    var i = 0
    var value
    $.each(orderedColumns, function (index, columnName) {
        // if (columnName == "Loan Amount") {
        //     value = amountFormatter(orderedValues[i]);
        value = orderedValues[i]

        // If NAICS code needs formatting:
        // if (columnName == "Industry (NAICS Code)") {
        //     value = colOptions["naicscode"][orderedValues[i]]
        // } else {
        //     value = orderedValues[i]
        // }
        html.push('<p><b>' + columnName + ':</b> ' + value + '</p>')
        i += 1
    })
    html.push('</div>')
    return html.join('')
}

function summaryDetailFormatter(index, row) {

    var summaryCols = {
        'state': 'State',
        'loancount': 'Number of Loans',
        'totaljobs': 'Number of Jobs'
    }
    var html = ['<div class="detailview">']
    $.each(row, function (key, value) {
        html.push('<p><b>' + summaryCols[key] + ':</b> ' + value + '</p>')
    })
    html.push('</div>')
    return html.join('')
}



// <!-- Reset table button -->
$(function() {
    $resetButton.click(function () {
        requestCount = 0
        initialConditions = true
        resetButtonClicked = true
        // $('table').bootstrapTable('clearFilterControl')

        document.querySelector("body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4 > div.fixed-table-toolbar > div.float-right.search.btn-group > div > input").value = ''
        var columns = Object.keys(orderedData)
        console.log(columns)
        for (column of columns) {
            $("#table").find("input.form-control.bootstrap-table-filter-control-" + column).val('')
            $('select[class*="bootstrap-table-filter-control-' + column + '"]').val('');
        }

        $('select[class*="bootstrap-table-filter-control-' + initialFilterColumn + '"]').val(initialFilterValue);
        $table.bootstrapTable('refresh')
    })
})

$(function() {
    $summaryResetButton.click(function () {
        console.log("CLICKED IT")
        $summaryTable.bootstrapTable('clearFilterControl')
    })
})





// <!-- Navigate back to Page 1 when the results per page selection changes -->
var currentPageSize = 10
var pageOneButton

$('#table').on('page-change.bs.table', function (pageSize, pageNumber) {
    selectedSize = document.querySelector("body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4 > div.fixed-table-pagination > div.float-left.pagination-detail > span.page-list > span > button > span.page-size").textContent.trim();
    if (currentPageSize != selectedSize) {
        document.querySelector(".fixed-table-body").scrollTop = 0;
        currentPageSize = selectedSize;
        $("[aria-label='to page 1']").click();
    }
});

// <!-- Change Toggle View text -->
$('#table').on('toggle.bs.table', function (cardView) {
    var toggleText = $('button[name ="toggle"]').contents().filter(function() {
        return this.nodeType == Node.TEXT_NODE;
    })
    if (toggleText.prevObject[1].data === ' Hide card view') {
        toggleText.prevObject[1].data = ' Show table view'
    }
});

// <!-- Loading screen overlay -->
    var type = 'bsGrow'
    function loadingTemplate(message) {
        if (type === 'fa') {
            return '<i class="spinner-text" color:#007aff;font-size:32px;">Doing government work...&nbsp;&nbsp;</i><i style="color:#007aff;" class="fa fa-spinner fa-spin fa-fw fa-2x spinner-spinner"></i>'
        }
        if (type === 'pl') {
            return '<div class="ph-item"><div class="ph-picture"></div></div>'
        }
        if (type === 'bsGrow') {
            return '<i class="spinner-text text-primary";">Doing government work...&nbsp;&nbsp;</i><i class="spinner-grow text-primary spinner-spinner" role="status"><span class="sr-only">Loading...</span></i>'
        }
    }
    
// <!-- Fix for Toggle All issue where table overlaps bottom pagination controls -->
$('#table').on('post-body.bs.table', function (e, arg1, arg2) {
    console.log('POST BODY RAN')
    $table.bootstrapTable('resetView')

    if (resetButtonClicked) {
        document.querySelector("body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4 > div.fixed-table-toolbar > div.float-right.search.btn-group > div > input").value = ''
        var columns = Object.keys(orderedData)
        for (column of columns) {
            $("#table").find("input.form-control.bootstrap-table-filter-control-" + column).val('')
            $('select[class*="bootstrap-table-filter-control-' + column + '"]').val('');
        }
        $('select[class*="bootstrap-table-filter-control-' + initialFilterColumn + '"]').val(initialFilterValue);
        resetButtonClicked = false;
    }
});

var preBodyRanCount = 0
$('#table').on('pre-body.bs.table', function (e, arg1, arg2) {
    console.log('PRE BODY RAN')
    // $('div.hidden').fadeIn(7000).removeClass('hidden');
    if (preBodyRanCount > 0) {
        $('div.hidden').fadeIn(500).removeClass('hidden');
    // setTimeout(() => { $('div.hidden').fadeIn(1000).removeClass('hidden'); }, 1);
    }
    console.log(preBodyRanCount)
    preBodyRanCount++;
});

$('#summary-table').on('pre-body.bs.table', function (e, arg1, arg2) {
    console.log('PRE BODY RAN')
    // $('div.hidden').fadeIn(7000).removeClass('hidden');
    if (preBodyRanCount > 0) {
        $('div.hidden').fadeIn(500).removeClass('hidden');
    // setTimeout(() => { $('div.hidden').fadeIn(1000).removeClass('hidden'); }, 1);
    }
    console.log(preBodyRanCount)
    preBodyRanCount++;

    if (requestCount == 0) {
        // Customize toggle switch text
        var toggleText = $('button[name ="toggle"]').contents().filter(function() {
            return this.nodeType == Node.TEXT_NODE;
        })
        if (toggleText.prevObject[1].data === ' Toggle') {
            toggleText.prevObject[1].data = " Show card view"
        }
    }
});

// Sidebar menu closing fix
var checkbox = document.querySelector("input[id=openSidebarMenu]");
var div = document.createElement('div');
div.id = 'left-nav-cover';

function sidebarMenuClick(element, eventName) {
    if (typeof checkbox != null) {
        document.addEventListener('click', function (e) {
            e = e || window.event;
            var target = e.target || e.srcElement;
            if ((target.getAttribute("id") != "sidebarMenu" && target.getAttribute("id") != "openSidebarMenu") && document.getElementById("openSidebarMenu").checked == true) {
                document.getElementById("openSidebarMenu").checked = false;
                sidebarMenuClick(checkbox, 'change');
            };
            if (target.getAttribute("id") == "openSidebarMenu" && document.getElementById("openSidebarMenu").checked == false) {
                document.getElementById("openSidebarMenu").checked = false;
                sidebarMenuClick(checkbox, 'change');
            };
        }, false);

        // function sidebarMenuClick(element, eventName) {
        //     var manualEvent = document.createEvent("HTMLEvents");
        //     manualEvent.initEvent(eventName, false, true);
        //     element.dispatchEvent(manualEvent);
        // }

        // var div = document.createElement('div');
        // div.id = 'left-nav-cover';
        document.getElementsByTagName('body')[0].appendChild(div);
        if (checkbox.checked) {
            div.innerHTML = "<div id='left-nav-cover-inner'></div>";
        } else {
            div.removeChild(document.getElementById("left-nav-cover-inner"));
        }
    }
}

// Cookie notification
if (localStorage.getItem('cookieSeen') != 'shown') {
    $('.cookie-box').delay(5000).fadeIn();
};

$('.cookie-close').click(function () {
    $('.cookie-box').fadeOut();
    localStorage.setItem('cookieSeen', 'shown')
})

// Hide initial page loader
$('#table').on('load-success.bs.table', function () {
    document.querySelector(".pre-table-spinner").style.display = "none";

});

// Scroll progress bar
$(window).scroll(function() {
    var scroll = $(window).scrollTop(),
    dh = $(document).height(),
    wh = $(window).height();
    scrollPercent = (scroll / (dh - wh)) * 100;
    $("#progressbar").css("height", scrollPercent + "%");
});

// Mobile Modal
// $('#myModal').on('shown.bs.modal', function () {
//     $('#myInput').trigger('focus')
// })

// $(window).on('load', function() {
//     $('#mobileModal').modal('show');
// });

$(document).ready(function(){
    console.log("INNER WIDTH:")
    console.log(window.innerWidth)
    if (window.innerWidth < 600) {
        console.log(window.innerWidth < 600)
        $("#mobileModal").modal('show');
    }
});


function summaryFormatterState() {
    return 'TOTAL'
}

function summaryFormatterNumberOfLoans(data) {
    var field = this.field
    return '$' + data.map(function (row) {
    return +row[field].substring(1)
    }).reduce(function (sum, i) {
    return sum + i
    }, 0)
}


console.log("\n\n\nUPDATED 1:41pm\n\n\n")

