import {Injectable} from "@angular/core";
import {CookieService} from "../services/cookie.service";

@Injectable({
  providedIn: 'root'
})
export class DbUserStore {
  private _username: string = "";
  private _password: string = "";

  constructor(private cookieService: CookieService) {
    let usernameCookie = cookieService.getCookie("dbUserName");
    let passwordCookie = cookieService.getCookie("dbPassword");
    if (usernameCookie) {
      this._username = usernameCookie;
    }
    if (passwordCookie) {
      this._password = passwordCookie;
    }
  }

  get username(): string {
    return this._username;
  }

  set username(value: string) {
    this.cookieService.createCookie("dbUserName", value, 365)
    this._username = value;
  }

  get password(): string {
    return this._password;
  }

  set password(value: string) {
    this.cookieService.createCookie("dbPassword", value, 365)
    this._password = value;
  }
}
