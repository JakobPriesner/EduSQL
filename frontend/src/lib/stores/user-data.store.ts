import {Injectable} from "@angular/core";
import {CookieService} from "../services/cookie.service";

@Injectable({
    providedIn: 'root'
})
export class UserDataStore {
    private _firstName: string = "";
    private _lastName: string = "";

    constructor(private cookieService: CookieService) {
        let firstNameCookie = cookieService.getCookie("firstName");
        let lastNameCookie = cookieService.getCookie("lastName");
        if (firstNameCookie) {
            this._firstName = firstNameCookie;
        }
        if (lastNameCookie) {
            this._lastName = lastNameCookie;
        }
    }


    get firstName(): string {
        return this._firstName;
    }

    set firstName(value: string) {
        this._firstName = value;
        this.cookieService.createCookie("firstName", value, 365)
    }

    get lastName(): string {
        return this._lastName;
    }

    set lastName(value: string) {
        this._lastName = value;
        this.cookieService.createCookie("lastName", value, 365)
    }
}
