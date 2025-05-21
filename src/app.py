from agents import Agent, Runner, trace
from dotenv import load_dotenv
import asyncio
from src.email_service.send_email import send_email

load_dotenv(override=True)

class ProfessionalSalesAgent:
    def __init__(self):
        self.name = "Professional Sales Agent"
        self.role = "A professional sales agent"
        self.instructions = "You're a sales agent working for TestCompany, a company that provides a SaaS tool for SOC 2 compliance and preparing for audits. \
            You write professional, serious emails that are likely to get a response. \
            Do not include any placeholders such as names, company names, or tokens — anywhere in the email (including subject lines, headers, or footers). \
            Keep it engaging, relevant, and funny — but with a clear call to action that fits the context of selling a SOC 2 compliance tool."

    def agent(self):
        return Agent(
            name=self.name,
            instructions=self.instructions,
            model="gpt-4o-mini"
        )

    def as_tool(self):
        return self.agent().as_tool(tool_name="write_email", tool_description="Write a cold sales email")

class WittySalesAgent:
    def __init__(self):
        self.name = "Witty Sales Agent"
        self.role = "A witty sales agent"
        self.instructions = "You're a humorous sales agent working for TestCompany, a company that provides a SaaS tool for SOC 2 compliance and preparing for audits. \
            You write witty, attention-grabbing emails that are likely to get a response. \
            Do not include any placeholders such as names, company names, or tokens — anywhere in the email (including subject lines, headers, or footers). \
            Keep it engaging, relevant, and funny — but with a clear call to action that fits the context of selling a SOC 2 compliance tool."

    def agent(self):
        return Agent(
            name=self.name,
            instructions=self.instructions,
            model="gpt-4o-mini"
        )

    def as_tool(self):
        return self.agent().as_tool(tool_name="write_email", tool_description="Write a witty, humorous cold sales email")


class BusySalesAgent:
    def __init__(self):
        self.name = "Busy Sales Agent"
        self.role = "A busy sales agent"
        self.instructions = "You're a busy sales agent working for TestCompany, \
            a company that provides a SaaS tool for SOC 2 compliance and preparing for audits. \
            You write witty, attention-grabbing emails that are likely to get a response. \
            Do not include any placeholders such as names, company names, or tokens — anywhere in the email (including subject lines, headers, or footers). \
            Keep it engaging, relevant, and funny — but with a clear call to action that fits the context of selling a SOC 2 compliance tool."

    def agent(self):
        return Agent(
            name=self.name,
            instructions=self.instructions,
            model="gpt-4o-mini"
        )

    def as_tool(self):
        return self.agent().as_tool(tool_name="write_email", tool_description="Write a concise, to the point cold sales email")

class SalesManager:
    def __init__(self):
        self.name = "Sales Manager"
        self.role = "A sales manager"
        self.instructions = "You're a sales manager working for TestCompany, \
            your job is to consider the sales agent's emails and \
            decide if they are good enough to send to the customer. \
            Try all the 3 emails and pick the best one. \
            Don't add extra information to the emails, just pick a single best email \
            and send it to the customer using the tool send_email."

    def run(self):
        with trace("Picks a best cold sales email"):
            return Agent(
                name=self.name,
                instructions=self.instructions,
                model="gpt-4o-mini",
                tools=[
                    ProfessionalSalesAgent().as_tool(),
                    WittySalesAgent().as_tool(),
                    BusySalesAgent().as_tool(),
                    send_email
                ]
            )

if __name__ == "__main__":
    async def main():
        with trace("Sales manager"):
            result = await Runner.run(SalesManager().run(), "Sends cold sales email addressed to the Company CEO")
            print(result)

    asyncio.run(main())
