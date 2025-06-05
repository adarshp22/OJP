from django.shortcuts import render
# Create your views here.
from .models import OJ,topic,CodeSubmission, problemset
from .forms import OJForm,UserRegistrationForm,CodeSubmitForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse
from .forms import CodeSubmissionForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path
import markdown
from django.utils.safestring import mark_safe
import tempfile
from google import genai
client = genai.Client(api_key= os.getenv('API_KEY'))

CPP_TEMPLATE = """#include <iostream>
using namespace std;

int main() {
    // Your code here
    return 0;
}
"""

PYTHON_TEMPLATE = """def main():
    # Your code here
    pass

if __name__ == "__main__":
    main()
"""


def oj_list(request):
    ojs=OJ.objects.all().order_by('-created_at')
    return render(request,'oj_list.html',{'ojs':ojs})

@login_required
def oj_create(request):
    if request.method=="POST":
        form=OJForm(request.POST,request.FILES)
        if form.is_valid():
            oj=form.save(commit=False)
            oj.user=request.user
            oj.save()
            return redirect('oj_list')
    else:
        form=OJForm()
    return render(request,'oj_form.html',{'form':form})    


@login_required
def oj_edit(request,oj_id):
    oj=get_object_or_404(OJ,pk=oj_id, user=request.user)
    if request.method=="POST":
        form=OJForm(request.POST,request.FILES,instance=oj)
        if form.is_valid():
            oj=form.save(commit=False)
            oj.user=request.user
            oj.save()
            return redirect('oj_list')
        
    else:
        form=OJForm(instance=oj)
    return render(request,'oj_form.html',{'form':form})    
        
@login_required
def oj_delete(request,oj_id):
    oj=get_object_or_404(OJ,pk=oj_id,user=request.user)
    if request.method=="POST":
        oj.delete()
        return redirect('oj_list')        
    return render(request,'oj_confirm_delete.html',{'oj':oj})   


def submit(request):
    submission = None
    output = None

    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user  # ✅ Set user
            output = run_code(
                submission.language, submission.code, submission.input_data
            )
            submission.output_data = output
            submission.save()
        selected_lang = form.cleaned_data.get("language", "py")
    else:
        selected_lang = request.GET.get("lang", "py")
        if selected_lang == "cpp":
            initial_code = CPP_TEMPLATE
        else:
            initial_code = PYTHON_TEMPLATE
            
        # form = CodeSubmissionForm()
        form = CodeSubmissionForm(initial={
            "language": selected_lang,
            "code": initial_code,
            "input_data": ""  # Optional: empty input field
        })
        

    return render(request, "index.html", {
        "form": form,
        "submission": submission,  # This enables result section to show
        "output": output,
        "selected_lang": selected_lang,
    })


def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)
    normalized_input = input_data.replace('\r\n', '\n').strip() + '\n'

    with open(input_file_path, "w") as input_file:
        # input_file.write(input_data)
        input_file.write(normalized_input)

    with open(output_file_path, "w") as output_file:
        pass  # This will create an empty file

    if language == "cpp":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ["g++", str(code_file_path), "-o", str(executable_path)]
        )
        if compile_result.returncode == 0:
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=output_file, 
                    )
    elif language == "py":
        # Code for executing Python script
        with open(input_file_path, "r") as input_file:
        
            with open(output_file_path, "w") as output_file:
                subprocess.run(
                    ["python", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                    stderr=output_file,
                )

    # Read the output from the output file
    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()

    return output_data






@login_required
def problem_topics(request):
    topics = topic.objects.all()
    return render(request, 'problem_topics.html', {'topics': topics})

@login_required
def topic_problems(request, id):
    selected_topic = get_object_or_404(topic, id=id)
    problems = selected_topic.problems.all()
    for prob in problems:
        prob.description_html = mark_safe(markdown.markdown(prob.description))
    return render(request, 'topic_problems.html', {'topic': selected_topic, 'problems': problems})
@login_required

def get_ai_review(code, language, problem_description):
    prompt = (
        f"Review the following {language} code for the problem:\n{problem_description}\n\n"
        f"Code:\n{code}\n\nProvide suggestions or improvements and write complete code in {language} provided."
        
    )
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # or "gemini-1" if you want
        contents=prompt,
        # optionally, you can set max_tokens or other parameters here if supported
    )
    
    return response.text

@login_required
def solve_problem(request, id):
    problem = get_object_or_404(problemset, id=id)
    problem.description_html = mark_safe(markdown.markdown(problem.description))
    output = None
    verdict = None
    error = None
    ai_suggestion = None

    if request.method == "POST":
        form = CodeSubmitForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            language = form.cleaned_data['language']   # You can extend this later for C++ or others
            input_data = problem.input_data.strip()
            expected_output = problem.expected_output.strip()
            action = request.POST.get('action')
            
            if action == "run":
                try:
                    output = run_code(language, code, input_data).strip()
                    verdict = (output == expected_output)
                    CodeSubmission.objects.create(
                        user=request.user,
                        problem=problem,
                        code=code,
                        language=language,
                        input_data=input_data,
                        output_data=output,
                    )
                except Exception as e:
                    error = str(e)
                    verdict = False
            elif action == "ai_review":
                # Prepare the prompt for Gemini AI
                prompt = (
                    f"Here is a coding problem:\n{problem.description}\n\n"
                    f"Here is the user's submitted code in {language}:\n{code}\n\n"
                    f"Please review the code and provide suggestions to improve\n "
                    f"point out possible bugs, or offer tips for correctness and efficiency\n."
                )
                
                try:
                    response = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt,
                    )
                    ai_suggestion = response.text
                except Exception as e:
                    error = f"AI Review failed: {str(e)}"
    else:
        form = CodeSubmitForm()
        
    return render(request, 'solve_problem.html', {
        'problem': problem,
        'form': form,
        'output': output,
        'verdict': verdict,
        'error': error,
        'ai_suggestion': ai_suggestion,
    })
            
            
            
    #         try:
    #             output = run_code(language, code, input_data).strip()
    #             verdict = (output == expected_output)
    #         except Exception as e:
    #             error = str(e)
    #             verdict = False
    # else:
    #     form = CodeSubmitForm()

    # return render(request, 'solve_problem.html', {
    #     'problem': problem,
    #     'form': form,
    #     'output': output,
    #     'verdict': verdict,
    #     'error': error
    # })

@login_required
def profile_view(request):
    user = request.user
    submissions = CodeSubmission.objects.filter(problem__isnull=False).filter(problem__topic__isnull=False)  # your filter may vary

    # Filter only user's submissions
    submissions = CodeSubmission.objects.filter(problem__isnull=False, problem__topic__isnull=False, user=user).select_related('problem')

    # Create a list of dicts with verdict calculated dynamically
    submissions_with_verdict = []

    for sub in submissions:
        if sub.problem:
            expected_output = sub.problem.expected_output.strip()
            actual_output = (sub.output_data or "").strip()
            verdict = (expected_output == actual_output)
        else:
            verdict = None

        submissions_with_verdict.append({
            'submission': sub,
            'verdict': verdict,
        })

    return render(request, 'profile.html', {
        'user': user,
        'submissions_with_verdict': submissions_with_verdict,
    })


def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('oj_list')            
    else:
        form =UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form}) 
        