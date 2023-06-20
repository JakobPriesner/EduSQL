import {Injectable} from "@angular/core";
import {CookieService} from "../services/cookie.service";

@Injectable({
  providedIn: 'root'
})
export class DbUserStore {
  private _username: string = "";
  private _password: string = "";

  constructor(private cookieService: CookieService) {
    let usernameCookie = cookieService.getCookie("firstName");
    let passwordCookie = cookieService.getCookie("lastName");
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
    this._username = value;
  }

  get password(): string {
    return this._password;
  }

  set password(value: string) {
    this._password = value;
  }
}
