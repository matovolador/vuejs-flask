
export const myMixin = {
    data () {
        return {
            refreshKey:0
        }
    },
    computed:{
        isLoggedIn(){
            this.refreshKey;
            return (this.xAccessToken !== undefined && this.xAccessToken != "" && this.xAccessToken != null) ? true : false
        },
        user(){
            this.refreshKey;
            return this.$cookies.get("user")
        },
        xAccessToken (){
            this.refreshKey;
            return this.$cookies.get('x-access-token')
        } 
    },
    methods: {
        setCookieToken (token){
            this.refreshKey++;
            if (this.refreshKey>20){
                this.refreshKey=0;
            }
            this.$cookies.set('x-access-token', token)
        },
        scrollToTop(top=0,left=0,immediate=false){
            //window.scrollTo(0,0);
            if (!immediate){
            window.scroll({
              top: top,
              left: left,
              behavior: 'smooth'
            })
        }else{
            window.scroll({
                top: top,
                left: left
              })
        }
          },

          getCharPosition(string, subString, index) {
            return string.split(subString, index).join(subString).length;
          },
          reloadPage(){
            this.refreshKey++;
            if (this.refreshKey>20){
                this.refreshKey=0;
            }
            this.scrollToTop(0,0,true)
            this.$router.go()
            
          },
          convertDateStringToLocale(dateString){
            let date = new Date(dateString)
            return date.toLocaleString()
          },
          dateToUniformString(date){
            let month = date.getMonth()+1
            if (month<10){
                month = "0"+month
            }
            let day = date.getDate()
            if (day<10){
                day = "0"+day
            }

            return ""+date.getFullYear()+"-"+month+"-"+day
          },
          isEmptyObject(obj) {
            var name;
            for (name in obj) {
                // eslint-disable-next-line
                if (obj.hasOwnProperty(name)) {
                    return false;
                }
            }
            return true;
        }
        
    },

  }