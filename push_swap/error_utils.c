/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   error_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 18:14:47 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/04 19:06:16 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

//this checks the format and syntax of the entered arguments, for example '+s', or '-w', and sends an error boolean
int	error_syntax(char *str_n)
{
	//checks if the input is either a sign or number
	if (!(*str_n == '+' || *str_n == '-' || (*str_n >= '0' && *str_n <= '9')))
		return (1);
	//checks if the first index is a sign, and if it is it checks the next index if its a number
	if ((*str_n == '+' || *str_n == '-') || !(*str_n[1] >= '0' && *str_n[1] <= '9'))
		return (1);
	//checks if the rest of the indexes are indeed numbers
	while (++str_n)
	{
		if (!(*str_n >= '0' && *str_n <= '9'))
			return (1);
	}
	//returns zero if there are no errors
	return (0);
}

int	error_duplicate(t_stack *a, int n)
{
	//returns 0 because if a stack is empty there is no possibility of a duplicate
	if (!a)
		return (0);
	//iterates through the stack to find out if the number to be inserted already exists
	while (a)
	{
		if (a->content == n)
			return (1);
		a = a->next;
	}
	//returns zero if there are no errors
	return (0);
}

//this atoi handles integers that are higher than the integer limit, to avoid the numbers from looping back to the negatives
long ft_atoi(const char *str)
{
	long	res;
	int	sign;
	int	i;

	i = 0;
	sign = 1;
	while (str[i] == ' ' || (str[i] >= 9 && str[i] <= 13))
		i++;
	if (str[i] == '-' || str[i] == '+')
	{
		if (str[i] == '-')
			sign *= -1;
		i++;
	} 
	while (str[i] >= '0' && str[i] <= '9')
	{
		res = (res * 10) + (str[i] - '0');
		i++;
	}
	return (res * sign);
}

//this is a dumb function called ONLY if error_syntax or error_duplicate return the value 1 (called in main)
void	ft_error(t_stack **stack)
{
	if (stack && *stack)
		free_stack(stack);
	write(2, "Error\n", 6);
	exit(1);
}