import {Injectable} from "@angular/core";
import {DbUserStore} from "../stores/db-user.store";
import {CookieService} from "../services/cookie.service";
import {LevelValidationResult} from "../models/levelValidationResult";

@Injectable({
    providedIn: 'root'
})
export class LocalRestrictionValidator {
    constructor(private dbUserStore: DbUserStore,
                private cookieService: CookieService) {
    }

    validateGetRestriction(level: number, task: number, expectedRestrictionState: string) : LevelValidationResult {
        if ("false" == expectedRestrictionState) {
            this.cookieService.createCookie("highestValidatedLevel", level + "." + task, 365);
            return {level: level + "." + task, isValid: true, message: ""};
        }
        let message: string = "The selection is unfortunately wrong. Check your SQL query again.";
        return {level: level + "." + task, isValid: false, message: message};
    }
}
