

    // <!-- Get column options -->
    var colOptions;
    
    function getColumnNames() {
        console.log("IN GET COLUMNS")
        // console.log(params)
        var request = new XMLHttpRequest();
        request.open('GET', 'http://localhost:5000/header_options/', false);  // `false` makes the request synchronous
        request.send(null);

        if (request.status === 200) {
            colOptions = JSON.parse(request.responseText);
        }
        console.log("Got column names.")
    }
    getColumnNames()


    // <!-- Reset button -->
    
        var $table = $('#table')
        var $resetButton = $('#resetButton')
    

    // <!-- Get data -->
        var $requestCount = 0
        console.log("COUNT REQUEST RESET TO 0")
        function ajaxRequest(params) {
            
            $('select[class*="bootstrap-table-filter-control-state"]').each(function(i) {
                if ($(this).children('option[selected="selected"]').length != 0) {
                    alert($(this).children('option[selected="selected"]').attr('value'));
                }
            });
            console.log('Request Count: ' + $requestCount)
            var url = '/params'
            console.log("HERE ARE THE PARAMS IN THE REQUEST:")
            console.log($.param(params.data))
            console.log("END PARAMS")
            // $.get(url + '?' + $.param(params.data))
            var requestParams
            var sortColumn = 'loanrange'
            var filterColumn = 'state'
            var filterValue = 'AK'
            if ($requestCount == 0) {
                requestParams = 'search=&sort='
                                + sortColumn
                                + '&order=asc&offset=0&limit=10&filter=%7B%22'
                                + filterColumn
                                + '%22%3A%22'
                                + filterValue
                                + '%22%7D'
                console.log("Manual params:")
                console.log(requestParams)
            } else {
                requestParams = $.param(params.data)
            }
            $.get(url + '?' + requestParams)
            
            .then(function (res) {
                params.success(res)
                console.log(res)
            });
            $requestCount++;
        };
    

    // <!-- Format loan amount data -->        
    
        function amountFormatter(value) {
            // return value.substring(0, value.length - 3)
            return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
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
                    return 'There are no loans in the center of that particular Venn diagram...<br><br>¯\\_(ツ)_/¯<br><br>but don\'t give up! Try it again with fewer filters.';
                },
                formatExport: function () {
                    return 'Export page'
                }
            };
            $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['en-US-custom']);
        })(jQuery);
    

    // <!-- Format data when a row is expanded -->
    

        var orderedData = {
            "loanamount": "Loan Amount ($)",
            "city": "City",
            "state": "State",                
            "zip": "ZIP Code",
            "naicscode": "NAICS Code",
            "businesstype": "Business Type",
            "raceethnicity": "Race/Ethnicity",
            "gender": "Gender",
            "veteran": "Veteran",
            "nonprofit": "Nonprofit",
            "jobsretained": "Jobs Retained",
            "dateapproved": "Date Approved",
            "lender": "Lender",
            "cd": "House District"
            }

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
                if (columnName == "Loan Amount ($)") {
                    value = amountFormatter(orderedValues[i]);
                } else {
                    value = orderedValues[i]
                }
                html.push('<p><b>' + columnName + ':</b> ' + value + '</p>')
                i += 1
            })
            html.push('</div>')
            return html.join('')
        }
    

    // <!-- Reset table button -->
    
        $(function() {
            $resetButton.click(function () {
                $table.bootstrapTable('destroy')
                $requestCount = 0
                console.log("REQUEST COUNT RESET TO 0 FROM RESET BUTTON")
                $table.bootstrapTable()
            })
        })
    

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
            $('div.hidden').fadeIn(2000).removeClass('hidden');
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


        $('#table').on('pre-body.bs.table', function (e, arg1, arg2) {
            console.log('PRE BODY RAN')
            $('div.hidden').fadeIn(2000).removeClass('hidden');

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