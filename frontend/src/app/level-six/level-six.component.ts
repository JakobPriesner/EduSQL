import { Component } from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {AbstractControl} from "@angular/forms";
import {MatStepper} from "@angular/material/stepper";
import {LocalRestrictionValidator} from "../../lib/validator/local-restriction.validator";

@Component({
  selector: 'app-level-six',
  templateUrl: './level-six.component.html',
  styleUrls: ['./level-six.component.scss']
})
export class LevelSixComponent {
  errorMessage: string = "";
  highestValidatedLevel: string = "0.0";
  restrictionGuess?: string = undefined;

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator, // todo: tmp delete
              private localRestrichtionValidator: LocalRestrictionValidator,
              private userDataStore: UserDataStore) {

  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to)) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }

  validateGetRestrictionTask(to: string, stepper: MatStepper) { // todo: evtl. PersonId angeben oder prüfen ob man Zugriff darauf hat
    if (this.restrictionGuess == undefined)
    {
      this.errorMessage += "The input field is empty!";
      return;
    }
    let validationResult = this.localRestrichtionValidator.validateGetRestriction(6, 2, this.restrictionGuess);
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.updateHighestValidationStep(validationResult.level, stepper);
    }
  }

  validateCreateRestrictionTask(to: string, stepper: MatStepper) {
    if (this.userDataStore.firstName == "" || this.userDataStore.lastName == "")
    {
      this.errorMessage += "Looks like you didn´t create a Student!";
      return;
    }
    let payload: { [key: string]: any } = {
      firstname: this.userDataStore.firstName,
      lastname: this.userDataStore.lastName
    };
    this.validationService.validateTaskWithPayload(6, 3, payload).subscribe(result => {
      if(result.isValid)
      {
        if (this.highestValidatedLevel.localeCompare(to)) {
          this.highestValidatedLevel =  to;
        }
        this.errorMessage = "";
        stepper.next();
      }
      else
        this.errorMessage = "Unfortunately, the permission has not yet been created. Please check your entry again.";
    });
  }
}
