import { Component } from '@angular/core';
import {MatStepper} from "@angular/material/stepper";
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";

@Component({
  selector: 'app-level-five',
  templateUrl: './level-five.component.html',
  styleUrls: ['./level-five.component.css']
})
export class LevelFiveComponent {

  errorMessage: string = "";
  highestValidatedLevel: string = this.cookieService.getCookie("highestValidatedLevel") ?? "0.0";

  constructor(public cookieService: CookieService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore,
              public validationService: ValidationService) {
    this.highestValidatedLevel = this.cookieService.getCookie("highestValidatedLevel") ?? "0.0";
  }

  validateDbUserLoginTask(stepper: MatStepper, task: number, expectedUser: string) {
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(5, task, expectedUser);
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.errorMessage = "";
      this.highestValidatedLevel = validationResult.level;
      stepper.next();
    }
  }

  validateLevel(stepper: MatStepper): void {

    this.validationService.validateTask(5, 2).subscribe(result => {
      if(!result.isValid)
      {
        this.errorMessage = result.message;
      } else {
        this.errorMessage = "";
        this.highestValidatedLevel = result.level;
        stepper.next();
      }
    });
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to)) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }

}
