import { Component } from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {LocalRestrictionValidator} from "../../lib/validator/local-restriction.validator";
import {MatStepper} from "@angular/material/stepper";

@Component({
  selector: 'app-level-eleven',
  templateUrl: './level-eleven.component.html',
  styleUrls: ['./level-eleven.component.scss']
})
export class LevelElevenComponent {
  errorMessage: string = "";
  highestValidatedLevel: string = this.cookieService.getCookie("highestValidationLevel") ?? "0.0";

  constructor(private cookieService: CookieService,
              private validationService: ValidationService) {

  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to) <= 0) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }

  validateUpdateExamAttemptGradeTask(to: string, stepper: MatStepper) {
    this.validationService.validateTask(11, 2).subscribe(result => {
      if(result.isValid)
      {
        if (this.highestValidatedLevel.localeCompare(to) <= 0) {
          this.highestValidatedLevel =  to;
        }
        this.errorMessage = "";
        stepper.next();
      } else {
        this.errorMessage = result.message;
      }
    });
  }
}
