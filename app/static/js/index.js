for (let i = 0; i < 10; i++) {
    callTable(i)
}

function callTable(i) {
    setTimeout(function() {
        $table.bootstrapTable();
        console.log('Table called time #' + i);
    }, 2000 * i);
}

    // <!-- Get column options -->
    var colOptions;
    
    function getColumnNames() {
        console.log("IN GET COLUMNS")
        // console.log(params)
        var request = new XMLHttpRequest();
        // request.open('GET', '/header_options', false);  // `false` makes the request synchronous
        request.open('GET', '/data/column_options.json', false);  // `false` makes the request synchronous
        request.send(null);

        if (request.status === 200) {
            colOptions = JSON.parse(request.responseText);
            console.log("GOT THEM...")
        }
        console.log("Got column names.")
    }
    getColumnNames()


    // <!-- Reset button -->
    var $table = $('#table')
    var $resetButton = $('#resetButton')
    

    // <!-- Get data -->
    var requestCount = 0
    var initial_state = true
    var requestParams
    var initialSortColumn
    var initialFilterColumn = 'state'
    var initialFilterValue = 'AK'
    var initialStateAddition
    var resetButtonClicked = false

    var page = window.location.href.split('//')[1].split('/')[1]

    console.log("COUNT REQUEST RESET TO 0")
    function ajaxRequest(params) {
        if(page.includes('data-150k-and-up')) {
            initialSortColumn = 'loanrange'
        } else if(page.includes('data-under-150k')) {
            initialSortColumn = 'loanamount'
        } else if(page.includes('all-data')) {
            initialSortColumn = 'loanamount'
        }

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
        console.log(params)
        params.data.filter = JSON.stringify(actualInputValues)
        console.log(params)

        var searchValue = document.querySelector("body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4 > div.fixed-table-toolbar > div.float-right.search.btn-group > div > input").value
        if (searchValue != '') {
            params.data.search = searchValue
        } else {
            delete params.data.search
        }


        $('select[class*="bootstrap-table-filter-control-state"]').each(function(i) {
            if ($(this).children('option[selected="selected"]').length != 0) {
                // alert($(this).children('option[selected="selected"]').attr('value'));
                console.log('there\'s a state!')
                // console.log($(this).children('option[selected="selected"]').attr('value'))
                // console.log(initialFilterValue)
                // console.log(($(this).children('option[selected="selected"]').attr('value') != initialFilterValue))
                if ($(this).children('option[selected="selected"]').attr('value') != initialFilterValue) {
                    initial_state = false;
                    console.log('Initial state set to false because a new state is chosen.');
                }
            } else {
                initial_state = false;
                console.log('Initial state is false because no state is chosen.')
            }
        });
        console.log('Request Count: ' + requestCount)
        var url = '/data'
        console.log("HERE ARE THE PARAMS IN THE REQUEST:")
        console.log($.param(params.data))
        console.log("END PARAMS")
        // $.get(url + '?' + $.param(params.data))

        if (requestCount == 0) {
            var toggleText = $('button[name ="toggle"]').contents().filter(function() {
                return this.nodeType == Node.TEXT_NODE;
            })
            if (toggleText.prevObject[1].data === ' Toggle') {
                toggleText.prevObject[1].data = " Show card view"
            }

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
            if (initial_state){
                console.log('STILL INITIAL STATE')
                console.log($.param(params.data))
                console.log($.param(params.data).includes('filter'))
                if ($.param(params.data).includes('filter')){
                    initialStateAddition = '%2C%22' + initialFilterColumn + '%22%3A%22' + initialFilterValue + '%22'
                    requestParams = $.param(params.data).substring(0, $.param(params.data).length - 3) + initialStateAddition + $.param(params.data).substring($.param(params.data).length - 3, $.param(params.data).length);
                } else {
                    initialStateAddition = '&filter=%7B%22' + initialFilterColumn + '%22%3A%22' + initialFilterValue + '%22%7D'
                    requestParams = $.param(params.data) + initialStateAddition;
                }
            } else {
            console.log('NOT INITIAL STATE ANYMORE')
            requestParams = $.param(params.data)
            }
        }
        console.log('The request params are: \r\n' + requestParams)
        console.log(url + '?' + 'page=' + page + '&' + requestParams)
        $.get(url + '?' + 'page=' + page + '&' + requestParams)
        
        .then(function (res) {
            params.success(res)
            console.log(res)
            var loanCount = res.total
            var jobsString = ' job'
            var pluralize = 's'
            if (loanCount > 1) {
                jobsString += pluralize
            }
            loanCount = numberWithCommas(loanCount)
            var loanTotal = res.footer.loanamountsum
            var jobsTotal = numberWithCommas(res.footer.jobsreportedsum)
            console.log(res.total)
            console.log(res.footer.loanamountsum)
            console.log(res.footer.jobsreportedsum)
            console.log("THAT WAS THE RES")
            var summary = ('The upshot: ' + loanCount + ' businesses received ' + loanTotal + ' to save ' + jobsTotal + jobsString + '.')
            // document.getElementById("summary").innerText = summary;
            var summaryDiv = document.getElementById("summary");
            console.log(summaryDiv)
            summaryDiv.innerHTML = summary;
            console.log(summary)
        });
        requestCount++;
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
                return "N/A";
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
                    return '<br>There are no loans in the center of that particular Venn diagram...<br><br>¯\\_(ツ)_/¯<br><br>but don\'t give up! Try it again with fewer filters.<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>';
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
                    values[i] = "N/A"
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
    
    // <!-- Reset table button -->
    
        $(function() {
            $resetButton.click(function () {


// var block_to_insert ;
// var container_block ;
 
// block_to_insert = document.createElement( 'div' );
// block_to_insert.innerHTML = 'This demo DIV block was inserted into the page using JavaScript.' ;
 
// container_block = document.getElementsByClassName("source");
// console.log(container_block)
// // container_block.append( block_to_insert );

// var newElement = document.createElement("div");
//     newElement.innerHTML = "my New Div Text";
// var myCurrentElement= document.getElementsByClassName('source');
//     // insertAfter(newElement, myCurrentElement);
//     myCurrentElement.innerHTML += "<h3>This is the text which has been inserted by JS</h3>"
//     console.log("DID IT")


   var tag = document.createElement("p");
   var text = document.createTextNode("Tutorix is the best e-learning platform");
   tag.appendChild(text);
   var element = document.getElementsByClassName("fixed-table-pagination");
   element.appendChild(tag);



            //     requestCount = 0
            //     initial_state = true
            //     resetButtonClicked = true
            //     // $('table').bootstrapTable('clearFilterControl')

            //     document.querySelector("body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4 > div.fixed-table-toolbar > div.float-right.search.btn-group > div > input").value = ''
            //     var columns = Object.keys(orderedData)
            //     console.log(columns)
            //     for (column of columns) {
            //         $("#table").find("input.form-control.bootstrap-table-filter-control-" + column).val('')
            //         $('select[class*="bootstrap-table-filter-control-' + column + '"]').val('');
            //         // console.log($("#table").find("input.form-control.bootstrap-table-filter-control-loanamount").val())
                    
            //         // $('select[class*="bootstrap-table-filter-control-' + column + '"]').each(function(i) {
            //         //     if ($(this).children('option[selected="selected"]').length != 0) {
            //         //         // alert($(this).children('option[selected="selected"]').attr('value'));
            //         //         // console.log('there\'s a state!')
            //         //         // console.log($(this).children('option[selected="selected"]').attr('value'))
            //         //         // console.log(initialFilterValue)
            //         //         // console.log(($(this).children('option[selected="selected"]').attr('value') != initialFilterValue))
            //         //         if ($(this).children('option[selected="selected"]').attr('value') != initialFilterValue) {
            //         //             initial_state = false;
            //         //             console.log('Initial state set to false because a new state is chosen.');
            //         //         }
            //         //     } else {
            //         //         initial_state = false;
            //         //         console.log('Initial state is false because no state is chosen.')
            //         //     }
            //         // });

            //     }

            //     $('select[class*="bootstrap-table-filter-control-' + initialFilterColumn + '"]').val(initialFilterValue);
            //     $table.bootstrapTable('refresh')
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
                console.log(columns)
                for (column of columns) {
                    $("#table").find("input.form-control.bootstrap-table-filter-control-" + column).val('')
                    $('select[class*="bootstrap-table-filter-control-' + column + '"]').val('');
                }
                $('select[class*="bootstrap-table-filter-control-' + initialFilterColumn + '"]').val(initialFilterValue);
                resetButtonClicked = false;
            }
        });

        // $('#table').on('toggle.bs.table', function (e, arg1, arg2) {
        //     console.log('TOGGLE RAN')
        //         $table.bootstrapTable('resetView')
        //         console.log("THIS THING HAPPENED")
        //     });
        // 

// <!-- 
// $('#table').on('all.bs.table', function (data, event) {
//     console.log(event)
//     // console.log(data)
//     // $table.bootstrapTable('resetView')

//     });
//  -->

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
                console.log("CHANGE")
            };
            if (target.getAttribute("id") == "openSidebarMenu" && document.getElementById("openSidebarMenu").checked == false) {
                document.getElementById("openSidebarMenu").checked = false;
                sidebarMenuClick(checkbox, 'change');
                console.log("CHANGE")
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
        // checkbox.addEventListener('change', function () {
            if (checkbox.checked) {
                div.innerHTML = "<div id='left-nav-cover-inner'></div>";
                console.log("CREATED")
            } else {
                div.removeChild(document.getElementById("left-nav-cover-inner"));
                console.log("REMOVED")
            }
        // });
    }
}
// End sidebar menu closing fix

// Cookie notification
    if (localStorage.getItem('cookieSeen') != 'shown') {
        $('.cookie-box').delay(5000).fadeIn();
    };

    $('.cookie-close').click(function () {
        $('.cookie-box').fadeOut();
        localStorage.setItem('cookieSeen', 'shown')
    })
// End cookie notification

// Hide initial page loader
$('#table').on('load-success.bs.table', function () {
    document.querySelector(".pre-table-spinner").style.display = "none";

});
// End hide initial page loader

// Scroll progress bar
$(window).scroll(function() {
  var scroll = $(window).scrollTop(),
  dh = $(document).height(),
  wh = $(window).height();
  scrollPercent = (scroll / (dh - wh)) * 100;
  $("#progressbar").css("height", scrollPercent + "%");
});
// End scroll progress bar

// var toggleButtonText = document.querySelector('body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4 > div.fixed-table-toolbar > div.columns.columns-right.btn-group.float-right > button')
// var toggleButtonText = document.querySelector("body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4 > div.fixed-table-toolbar > div.columns.columns-right.btn-group.float-right > button > i")
var toggleButtonText = $( "[name='toggle']" )
console.log("TOGGLE JQUERY TEXT:")
console.log(toggleButtonText.innerHTML)
toggleButtonText.onload = function(){
    console.log("TOGGLE BUTTON:")
    console.log(toggleButtonText.innerHTML)
    toggleButtonText.innerHTML = "NEW BUTTON TEXT"
}
// console.log(document.evaluate(
//     '/html/body/div[3]/div[5]/div[1]/div[1]/div[2]/button',
//     document,
//     null,
//     XPathResult.ANY_TYPE,
//     null))
// var toggleItem = $x(toggleText)
// console.log(toggleItem)


// body > div.changing-content > div.outside > div.bootstrap-table.bootstrap4


console.log("THAT WAS THE ITEM")
// Prevent scrolling when clicking into a card view
document.getElementsByClassName('fa').addEventListener('click', function (e) {
    e.preventDefault();
})
// End prevent scrolling when clicking into a card view

