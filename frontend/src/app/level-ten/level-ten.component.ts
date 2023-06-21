import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import {CookieService} from "../../lib/services/cookie.service";
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";
import {ValidationService} from "../../lib/services/api/validation.service";

@Component({
  selector: 'app-level-ten',
  templateUrl: './level-ten.component.html',
  styleUrls: ['./level-ten.component.scss'],
  providers: [
      {
          provide: STEPPER_GLOBAL_OPTIONS,
          useValue: {showError: true},
      },
  ]
})
export class LevelTenComponent {
    public validationFormGroup: FormGroup;
    public errorMessage: string = "";

    constructor(private formBuilder: FormBuilder,
                public cookieService: CookieService,
                private validationService: ValidationService){
        this.validationFormGroup = this.formBuilder.group({
            matriculationNumber: ['', Validators.required],
            averageGrade: ['', Validators.required]
        });
    }

    validateLevel(): void {
        if (!this.validationFormGroup.valid) {
            this.errorMessage = "The input field is empty!";
            return;
        }
        let payload: { [key: string]: any } = {
            matriculationNumber: this.validationFormGroup.get("matriculationNumber")?.value,
            averageGrade: this.validationFormGroup.get("averageGrade")?.value
        };
        this.validationService.validateTaskWithPayload(10, 1, payload).subscribe(result => {
            if(!result.isValid)
            {
                this.errorMessage = result.message;
            } else {
                this.errorMessage = "";
            }
        });
    }
}
