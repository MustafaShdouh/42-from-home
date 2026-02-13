/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils_lib.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/06 21:02:45 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/13 23:59:40 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"
#include "libft.h"

void	index_stack(t_stack *stack)
{
	t_stack	*ptr;
	t_stack	*runner;
	int		count;

	ptr = stack;
	while (ptr)
	{
		count = 0;
		runner = stack;
		while (runner)
		{
			if (runner->content < ptr->content)
				count++;
			runner = runner->next;
		}
		ptr->index = count;
		ptr = ptr->next;
	}
}

long ft_atol(const char *str)
{
	long	res;
	int	sign;
	int	i;

	res = 0;
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

void	ft_putfloat_fd(double num, int fd)
{
	int	int_part;
	int	dec_part;

	if (num < 0)
	{
		write(fd, "-", 1);
		num = -num;
	}
	int_part = (int)num;
	dec_part = (int)((num - int_part) * 100);
	ft_putnbr_fd(int_part, fd);
	write(fd, ".", 1);
	if (dec_part < 10)
		write(fd, "0", 1);
	ft_putnbr_fd(dec_part, fd);
}

int	ft_strcmp(const char *s1, const char *s2)
{
	size_t	i;

	i = 0;
	while (s1[i] && s1[i] == s2[i])
		i++;
	return ((unsigned char)s1[i] - (unsigned char)s2[i]);
}
