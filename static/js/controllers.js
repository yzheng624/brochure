// Remember: Quick and dirty
var app = angular.module('brochureApp', ['ngRoute', 'ngResource', 'ngSanitize', 'xeditable'],
  function($routeProvider, $locationProvider) {
    $routeProvider.when('/', {
      templateUrl: '/welcome.html',
      controller: 'mainCntl',
      controllerAs: 'main'
    });
    $routeProvider.when('/store/:store_name/product', {
      templateUrl: '/product.html',
      controller: 'mainCntl',
      controllerAs: 'main'
    });
    $routeProvider.when('/store/:store_name/product/:action', {
      templateUrl: '/add_product.html',
      controller: 'mainCntl',
      controllerAs: 'main'
    });
    $routeProvider.when('/store/:store_name/:page_name', {
      templateUrl: '/page.html',
      controller: 'mainCntl',
      controllerAs: 'main'
    });
    $routeProvider.when('/store/:store_name/:page_name/show/:pk', {
      templateUrl: '/page_products.html',
      controller: 'mainCntl',
      controllerAs: 'main'
    });
    $routeProvider.when('/store/:store_name/:page_name/:action', {
      templateUrl: '/add_page.html',
      controller: 'mainCntl',
      controllerAs: 'main'
    });
    $routeProvider.otherwise({
      redirectTo: '/'
    });

    // configure html5 to get links working on jsfiddle
    $locationProvider.html5Mode(true);
});

app.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

app.factory('productFactory', ['$http', function ($http) {
    var urlBase = '/';
    var productFactory = {};

    productFactory.query = function (url, store_name) {
        data = {'url': url, 'store_name': store_name};
        return $http.post(urlBase + 'query/', data);
    };

    productFactory.addItem = function (data, store_name) {
        data.store_name = store_name;
        return $http.post(urlBase + 'add_item/', data);
    };

    productFactory.getAll = function (store_name) {
        data = {'store_name': store_name};
        return $http.post(urlBase + 'get_items/', data);
    };

    productFactory.getWatchlist = function (store_name) {
        data = {'store_name': store_name};
        return $http.post(urlBase + 'get_watchlist/', data);
    };

    productFactory.deleteItems = function (selected) {
        return $http.post(urlBase + 'delete_items/', selected);
    };

    productFactory.dummy = function () {
        return $http.get(urlBase + 'sync/');
    };

    productFactory.setMark = function (data) {
        return $http.post(urlBase + 'set_mark/', data);
    };

    productFactory.updatePrice = function (data) {
        return $http.post(urlBase + 'update_price/', data);
    };

    productFactory.addPage = function (data, store_name) {
        data.store_name = store_name;
        return $http.post(urlBase + 'add_page/', data);
    };

    productFactory.getAllPages = function (store_name) {
        data = {'store_name': store_name};
        return $http.post(urlBase + 'get_pages/', data);
    };

    productFactory.getPageProduct = function (pk) {
        data = {
            'pk': pk
        };
        return $http.post(urlBase + 'get_page_products/', data);
    };

    productFactory.updateDescription = function (data) {
        return $http.post(urlBase + 'update_description/', data);
    };

    productFactory.deletePages = function (data) {
        return $http.post(urlBase + 'delete_pages/', data);
    }

    return productFactory;
}]);

app.controller('mainCntl', ['$scope', 'productFactory', '$routeParams', '$location', function ($scope, productFactory, $routeParams, $location) {
    console.log($routeParams);
    $scope.store_name = $routeParams['store_name'];
    var opts = {
            lines : 13, // The number of lines to draw
            length : 7, // The length of each line
            width : 4, // The line thickness
            radius : 10, // The radius of the inner circle
            corners : 1, // Corner roundness (0..1)
            rotate : 0, // The rotation offset
            color : '#000', // #rgb or #rrggbb
            speed : 1, // Rounds per second
            trail : 60, // Afterglow percentage
            shadow : false, // Whether to render a shadow
            hwaccel : false, // Whether to use hardware acceleration
            className : 'spinner', // The CSS class to assign to the spinner
            zIndex : 2e9, // The z-index (defaults to 2000000000)
            top : $(window).height()/2.5, // Manual positioning in viewport
            left : "auto"
    };
    productFactory.dummy();
    $scope.predicate = 'fields.current_price';
    $scope.reverse = false;
    $scope.info = 'Something is wrong.';
    $scope.itemClicked = function (store_name) {
        $scope.store_name = store_name;
        $('li').removeClass('active');
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        productFactory.getAll(store_name).success(function (products) {
            productFactory.getWatchlist(store_name).success(function (watchlist) {
                for (var i = 0; i < products.length; i++) {
                    products[i].fields.original_price = parseFloat(products[i].fields.original_price);
                    products[i].fields.current_price = parseFloat(products[i].fields.current_price);
                    if (products[i].fields.error == true) {
                        products[i].fields.error_text = 'Error';
                    } else {
                        products[i].fields.error_text = products[i].fields.last_update;
                    }
                    for (var j = 0; j < watchlist.length; j++) {
                        if (products[i].pk === watchlist[j].fields.product) {
                            products[i].fields.desire_price = watchlist[j].fields.desire_price;
                            products[i].fields.mark = watchlist[j].fields.mark;
                        }
                    }
                }
            });
            $scope.spinner.stop();
            $scope.products = products;
        });
        $('#' + store_name +'List').addClass('active');
    };
    if ($routeParams['store_name'] && !$routeParams['action'] && !$routeParams['page_name']) {
        $scope.itemClicked($routeParams['store_name']);
    }
    $scope.addLink = function () {
        $scope.info = 'Something is wrong.';
        $('#url').val('');
        $('#menubar').hide();
        $('#hr').hide();
        $('#table').hide();
        $('#addLink').show();
        $('#addLinkNext').show();
        $('#addLinkDetail').hide();
    };
    $scope.addLinkNext = function () {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        productFactory.query($scope.new.queryUrl, $scope.store_name).success(function (product) {
            $scope.spinner.stop();
            if (product.info != '') {
                $scope.info = product.info;
                $('#info').modal('show');
            } else {
                url = $scope.new.queryUrl;
                $scope.new = product;
                $scope.new.queryUrl = url;
                $('#addLinkNext').hide();
                $('#addLinkDetail').show();
            }
        }).error(function () {
            $scope.spinner.stop();
            $('#info').modal('show');
        });
    };
    $scope.submitProduct = function () {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'url': $scope.new.queryUrl,
            'desire_price': $scope.new.desire_price,
            'current_price': $scope.new.current_price,
            'original_price': $scope.new.original_price,
            'name': $scope.new.name,
            'email': $scope.new.email,
            'uuid': $scope.new.uuid
        };
        productFactory.addItem(data, $scope.store_name).success(function (info) {
            $scope.spinner.stop();
            $location.path('/store/' + $scope.store_name);
        });
    };
    $scope.selected = {};
    $scope.deleteItems = function () {
        productFactory.deleteItems($scope.selected).success(function (info) {
            $scope.itemClicked($scope.store_name);
        });
    };
    $scope.selectAll = function () {
        console.log($('.selectAll').is(':checked'));
        if ($('.selectAll').is(':checked')) {
            for (var i = 0; i < $scope.products.length; i++) {
                $scope.selected[$scope.products[i].pk] = true;
            }
        } else {
            for (var i = 0; i < $scope.products.length; i++) {
                $scope.selected[$scope.products[i].pk] = false;
            }
        }
    };
    $scope.markClicked = function (pk) {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'pk': pk,
        }
        productFactory.setMark(data).success(function (info) {
            $scope.spinner.stop();
        });
    };
    $scope.updatePrice = function (pk, desire_price) {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'pk': pk,
            'desire_price': desire_price
        };
        productFactory.updatePrice(data).success(function (info) {
            $scope.spinner.stop();
        });
    };
    $scope.submitPage = function () {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'url': $scope.new.url,
            'description': $scope.new.description,
            'least_price': $scope.new.least_price,
            'discount': $scope.new.discount_percentage,
            'email': $scope.new.email
        };
        productFactory.addPage(data, $scope.store_name).success(function (info) {
            $scope.spinner.stop();
            $location.path('/store/' + $scope.store_name +'/page');
        }).error(function () {
            $scope.spinner.stop();
            $('#info').modal('show');
        });
    };
    $scope.pageClicked = function (store_name) {
        $scope.store_name = store_name;
        $('li').removeClass('active');
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        productFactory.getAllPages(store_name).success(function (pages) {
            $scope.selected = {};
            for (var i = 0; i < pages.length; i++) {
                $scope.selected[pages[i].pk] = false;
                pages[i].fields.discount_amount = parseFloat(pages[i].fields.original_price) - parseFloat(pages[i].fields.current_price);
                pages[i].fields.discount_percentage = parseFloat(pages[i].fields.discount_amount) / parseFloat(pages[i].fields.original_price);
                pages[i].fields.status_text = 'Last Update: ' + pages[i].fields.last_update + ' | Total: ' + pages[i].fields.product.length + ' | Error: todo';
            }
            $scope.spinner.stop();
            $scope.pages = pages;
        });
        $('#' + store_name +'List').addClass('active');
    };
    if ($routeParams['pk']) {
        productFactory.getPageProduct($routeParams['pk']).success(function (products) {
            for (var i = 0; i < products.length; i++) {
                products[i].fields.original_price = parseFloat(products[i].fields.original_price);
                products[i].fields.current_price = parseFloat(products[i].fields.current_price);
                products[i].fields.discount_amount = Math.round(((products[i].fields.original_price) - (products[i].fields.current_price)) * 100) / 100;
                products[i].fields.discount_percentage = Math.round((products[i].fields.discount_amount) / (products[i].fields.original_price) * 100) / 100;
            }
            $scope.products = products;
        });
    }
    else if ($routeParams['store_name'] && !$routeParams['action'] && $routeParams['page_name']) {
        $scope.pageClicked($routeParams['store_name']);
    }
    $scope.clearActive = function () {
        $('li').removeClass('active');
    };
    $scope.updateDescription = function (pk, description) {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'pk': pk,
            'description': description
        };
        productFactory.updateDescription(data).success(function (info) {
            $scope.spinner.stop();
        }).error(function (info) {
            $scope.spinner.stop();
            $('#info').modal('show');
        });
    };
    $scope.deletePages = function () {
        console.log($scope.selected);
        productFactory.deletePages($scope.selected).success(function (info) {
            $location.path('/store/' + $routeParams['store_name'] + '/' + $routeParams['page_name']);
        });
    };
    $scope.updateLeastPrice = function (pk, least_price) {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'pk': pk,
            'least_price': least_price
        };
        productFactory.updateLeastPrice(data).success(function (info) {
            $scope.spinner.stop();
        }).error(function (info) {
            $scope.spinner.stop();
            $('#info').modal('show');
        });
    };
    $scope.updateDiscount = function (pk, discount) {
        var target = $("body")[0];
        $scope.spinner = Spinner(opts).spin(target);
        data = {
            'pk': pk,
            'discount': discount
        };
        productFactory.updateDiscount(data).success(function (info) {
            $scope.spinner.stop();
        }).error(function (info) {
            $scope.spinner.stop();
            $('#info').modal('show');
        });
    };
}]);