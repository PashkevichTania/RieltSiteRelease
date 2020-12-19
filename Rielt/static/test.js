new Vue({
        el: '#test',
        data: {
            temp:null,
            emp: null,
            employees: [],
        },
        created: function () {
            axios.get('/api/employees/')
                .then(function (response) {
                    this.employees = response.data
                    console.log(response.data)
                })
        },
        methods: {
            find: function () {

            }
        },
    }
)