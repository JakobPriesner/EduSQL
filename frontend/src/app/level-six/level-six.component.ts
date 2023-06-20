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
  styleUrls: ['./level-six.component.css']
})
export class LevelSixComponent {
  errorMessage: string = "";
  highestValidatedLevel: string = "0.0";
  boolValue: boolean[] = [
      true, false
  ]
  restrictionGuess?: string = undefined;

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              private localRestrichtionValidator: LocalRestrictionValidator) {

  }

  ngOnInit() {

  }

  cookieValidator(control: AbstractControl): { [key: string]: any } | null {
    const formValue = control.value;
    const cookieValue = this.cookieService.getCookie('cookieName');
    if (cookieValue == null) {
      return { 'cookieExists': false };
    }
    return cookieValue.localeCompare(formValue) >= 0 ? null : { 'stepValidated': false };
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to)) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }

  validateRestrictionTask(to: string, stepper: MatStepper) {
    if (this.restrictionGuess == undefined)
    {
      this.errorMessage += "The input field is empty!";
      return;
    }
    let validationResult = this.localRestrichtionValidator.validateRestriction(6, 2, this.restrictionGuess);
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.updateHighestValidationStep(validationResult.level, stepper);
    }
  }
}
