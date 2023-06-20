import {Injectable} from "@angular/core";
import {DbUserStore} from "../stores/db-user.store";
import {CookieService} from "../services/cookie.service";
import {LevelValidationResult} from "../models/levelValidationResult";

@Injectable({
    providedIn: 'root'
})
export class LocalDbUserValidator {
    constructor(private dbUserStore: DbUserStore,
                private cookieService: CookieService) {
    }

    validateLoggedInAsUser(level: number, task: number, expectedUsername: string) : LevelValidationResult {
        if (this.dbUserStore.username == expectedUsername) {
            this.cookieService.createCookie("highestValidatedLevel", level + "." + task, 365);
            return {level: level + "." + task, isValid: true, message: ""};
        }
        let message: string = "You are not signed in as \"" + expectedUsername + "\". Please perform the regarding steps and try again.";
        if (this.dbUserStore.username != "") {
            message = "You are currently signed in as \"" + this.dbUserStore.username + "\" instead of \"" + expectedUsername + "\". Please perform the regarding steps and try again.";
        }
        return {level: level + "." + task, isValid: false, message: message};
    }
}
