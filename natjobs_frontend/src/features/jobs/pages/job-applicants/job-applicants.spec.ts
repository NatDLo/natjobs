import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { of } from 'rxjs';
import { ApplicationService } from '../../../../core/services/application.service';

import { JobApplicantsComponent } from './job-applicants';

describe('JobApplicantsComponent', () => {
	let component: JobApplicantsComponent;
	let fixture: ComponentFixture<JobApplicantsComponent>;

	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [JobApplicantsComponent],
			providers: [
				provideHttpClient(),
				{
					provide: ActivatedRoute,
					useValue: {
						snapshot: {
							params: {
								id: '1',
							},
						},
					},
				},
				{
					provide: ApplicationService,
					useValue: {
						updateStatus: () => of({}),
					},
				},
			],
		}).compileComponents();

		fixture = TestBed.createComponent(JobApplicantsComponent);
		component = fixture.componentInstance;
		await fixture.whenStable();
	});

	it('should create', () => {
		expect(component).toBeTruthy();
	});
});
